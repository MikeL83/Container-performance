/*
 * File:   main.cpp
 *
 * The purpose of the program is to compare std::vector and std::list.
 * The program generates a sequence of random numbers which it then
 * inserts and removes from the given container.
 *
 * Author: Mikko Leppänen
 *
 * Created on 20. joulukuuta 2014, 16:38
 */

#include <algorithm>
#include <boost/container/list.hpp>
#include <boost/container/slist.hpp>
#include <boost/container/stable_vector.hpp>
#include <boost/container/vector.hpp>
#include <chrono>
#include <cstdlib>
#include <exception>
#include <forward_list>
#include <functional>
#include <future>
#include <iostream>
#include <iterator>
#include <list>
#include <ostream>
#include <random>
#include <string>
#include <thread>
#include <type_traits>
#include <utility>
#include <vector>

using namespace std;

template <typename Container, typename Func>
void processContainer(Func &&f, int N)
{
    random_device rndDevice;
    mt19937 eng(rndDevice());
    uniform_int_distribution<int> dist(1, N);
    auto gen = bind(dist, eng);
    Container seq(N);

    generate(seq.begin(), seq.end(), gen);

    f(seq);
}

void analyze(const string &cont, int N)
{
    auto f_list = [&](auto &&seq) {
        seq.sort();
        random_device rndDevice;
        mt19937 eng(rndDevice());
        while (seq.size() > 0) {
            uniform_int_distribution<int> dist(0, seq.size() - 1);
            auto gen = bind(dist, eng);
            auto range_begin = begin(seq);
            advance(range_begin, gen());
            seq.erase(range_begin);
        }
    };
    auto f_vector = [&](auto &&seq) {
        sort(seq.begin(), seq.end());
        random_device rndDevice;
        mt19937 eng(rndDevice());
        while (seq.size() > 0) {
            uniform_int_distribution<int> dist(0, seq.size() - 1);
            auto gen = bind(dist, eng);
            seq.erase(begin(seq) + gen());
        }
    };
    auto f_forwardlist = [&](auto &&seq) {
        seq.sort();
        random_device rndDevice;
        mt19937 eng(rndDevice());
        while (!seq.empty()) {
            uniform_int_distribution<int> dist(
                0, distance(seq.begin(), seq.end()) - 1);
            auto gen = bind(dist, eng);
            auto range_begin = seq.before_begin();
            advance(range_begin, gen());
            seq.erase_after(range_begin);
        }
    };

    if (cont == "std::list") {
        processContainer<list<int>>(f_list, N);
    } else if (cont == "boost::list") {
        processContainer<boost::container::list<int>>(f_list, N);
    } else if (cont == "boost::slist") {
        processContainer<boost::container::slist<int>>(f_list, N);
    } else if (cont == "std::vector") {
        processContainer<vector<int>>(f_vector, N);
    } else if (cont == "boost::vector") {
        processContainer<boost::container::vector<int>>(f_vector, N);
    } else if (cont == "boost::stable_vector") {
        processContainer<boost::container::stable_vector<int>>(f_vector, N);
    } else if (cont == "std::forward_list") {
        processContainer<forward_list<int>>(f_forwardlist, N);
    } else {
        cerr << "There is some ambiguous in container name." << endl;
        cerr << "Acceptable container arguments: list, vector or forward_list"
             << std::endl;
        cerr << "Execution failed." << std::endl;
    }
}

int main(int argc, char *argv[])
{
    string container;
    int number_of_elements;
    if (argc !=
        3) { // Program expect 3 arguments: the program name, the source path
             // and the destination path
        cerr << "Usage: " << argv[0] << " N(number of elements) "
             << " Container(std::vector, std::list, boost::vector, boost::list,"
                " boost::stable_vector, boost::slist or std::forward_list)"
             << std::endl;
        return 1;
    }
    number_of_elements = abs(atoi(argv[1]));
    container = argv[2];
    transform(container.begin(), container.end(), container.begin(), ::tolower);
    if (container == "std::list") {
        cout << "std::list type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "boost::list") {
        cout << "boost::list type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "boost::slist") {
        cout << "boost::list type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "std::vector") {
        cout << "std::vector type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "boost::vector") {
        cout << "std::vector type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "boost::stable_vector") {
        cout << "std::vector type was chosen and number of elements is "
             << number_of_elements << endl;
    } else if (container == "std::forward_list") {
        cout << "std::forward_list type was chosen and number of elements "
                "is "
             << number_of_elements << endl;
    }
    cout << "Waiting for program to finish..." << endl;

    // calculate average of five runs
    std::vector<double> timings;
    int runs = 5;
    if (number_of_elements > 10000) {
        runs = 2;
    }
    for (int k = 0; k < runs; k++) {
        auto start_t = chrono::duration_cast<chrono::nanoseconds>(
                           chrono::steady_clock::now().time_since_epoch())
                           .count(); // chrono::system_clock::now();
        // run function asynchronously
        auto f = async(launch::async, analyze, container, number_of_elements);
        if (f.wait_for(chrono::seconds(0)) == future_status::deferred) {
            cout << "Execution deferred" << endl;
        } else {
            f.wait();
        }
        auto end_t = chrono::duration_cast<chrono::nanoseconds>(
                         chrono::steady_clock::now().time_since_epoch())
                         .count();
        auto diff = end_t - start_t;
        timings.emplace_back(
            static_cast<double>(chrono::duration<double, milli>(diff).count()) *
            1e-9);
    }
    double average = 0.0;
    for (const auto &t : timings) {
        average += t;
    }
    average = average / static_cast<double>(runs);
    cout << average << "\n";

    return 0;
}

/*
while (f.wait_for(chrono::milliseconds(100)) != future_status::ready) {
    cout << "Execution ready" << endl;
    // end timing and collect show execution time
    auto end_t = chrono::system_clock::now();
    auto diff = end_t - start_t;
    cout << "Execution time: " << chrono::duration<double, milli>(diff).count()
         << " ms" << endl;
    return 0;
}
*/
