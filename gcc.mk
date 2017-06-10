# --*--Makefile for C++ codes--*--
#
# Mikko Leppanen 2017

SHELL := /bin/sh

#Compiling
# GCC
CXX := g++-7
# Clang
#CXX := clang++-3.9
INCLS := -I #/home/mikko/sw/include/benchmark/include
CPPFLAGS := -MMD -MP $(INCLS)
WARN := -Wall -pedantic -Werror -Wextra
OPTIM := -O3 -m64 -mtune=intel \
	     -fno-omit-frame-pointer -fno-exceptions\
		 -fno-rtti # -ftree-parallelize-loops=2
DEBUG := -ggdb
PROF := -g -pg
ifeq ($(CXX),g++-7)
    CXXFLAGS := -std=c++1z -libstd=c++ -fdiagnostics-color=always $(OPTIM) $(WARN)
else
    CXXFLAGS := -std=c++1z -stdlib=libc++ -fdiagnostics-color=always $(OPTIM) $(WARN)
endif
TARGET_ARCH := -march=corei7-avx
COMPILE = $(CXX) -I/home/mikko/sw/include $(INCLS) $(CXXFLAGS) $(TARGET_ARCH) -c -MMD -MP -MF  

#Linking
LD := $(CXX)
LDFLAGS := -pthread -lpthread -lc++abi -lc++ #-lbenchmark
#LDLIBS := #-L/home/mikko/5.5/gcc_64/lib  #-L/home/mikko/sw/include/benchmark
#LOADLIBES :=

EXENAME := nsequencebench
SCR := nsequencebench.cpp
OBJS := $(SCR:.cpp=.o)
DEPS := $(SCR:.cpp=.d)
HDRS := 

.SUFFIXES:
.SUFFIXES: .cpp .o .h

all:$(EXENAME)


%.o%.d: %.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: C++ Compiler'
	$(COMPILE) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; $(RM) -rf $@.$$$$
	@echo 'Finished building: $<'
	@echo ' '

$(EXENAME): $(OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: C++ Linker'
	$(LD) $(LDFLAGS) -o $@ $^ $(LDLIBS)
	@echo 'Finished building target: $@'
	@echo ' '

.PHONY: all clean help

help:
	$(MAKE) --print-data-base --question 
#$(AWK) '/^[^.%][-A-Za-z0-9_]*:/ \{ print substr($$1,1,length($$1)-1) }'
#$(SORT) | \
#$(PR) --omit-pagination --width=80 --columns=4

clean:
	@echo 'Cleaning...'
	$(RM) $(EXENAME) $(OBJS) core 
	@echo ' '

#clobber: clean
#	rm -f $(EXENAME)

