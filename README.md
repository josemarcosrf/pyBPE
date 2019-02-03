# fastBPE python wrapper

This repo it is based on [fastBPE](https://github.com/glample/fastBPE) modified to expose similar function working using input strings instead of files.

More specifically exposes the following funtions:

```python
import libpybpe as bpe

text = "This is a test sentence to test test"

# get_vocabs: equivalent to getvocab
print(bpe.get_vocabs(text))
{'This': 1, 'a': 1, 'is': 1,
 'sentence': 1, 'test': 3, 'to': 1}

# learn_bpe: equivalent to learnbpe
print(bpe.learn_bpes(5, text))
[('t', 'e', 4),
 ('s', 't</w>', 3),
 ('te', 'st</w>', 3),
 ('i', 's</w>', 2),
 ('t', 'o</w>', 1)]
```

## Requirements

-   [Boost==1.69](http://www.boost.org/)
-   [CMake>=3.13](https://cmake.org/download/)
-   g++ compiler (>=5.4.0)
-   python (>=3.6)
-   [anaconda3](https://www.continuum.io/downloads)

## How to

### C++

To compile the code without the python wrapper:

```bash
    # compile without python wrapper
    g++ -std=c++11 -pthread -O3 fast.cpp -o fast
```

### Python

1. Download and install Boost
   (Here we assume we are using Anaconda in an environment called `testDL` with python 3.6)

```bash
    # download and extract
    cd Downloads
    wget https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.bz2
    tar --bzip2 -xf boost_1_69_0.tar.bz2
    cd boost_1_69_0/

    # soft links to the names expected by boost
    ln -s ~/anaconda3/include/python3.6m/ ~/anaconda3/include/python3.6/
    ln -s ~/anaconda3/envs/testDL/include/python3.6m/ ~/anaconda3/envs/testDL/include/python3.6/

    python_root=`python -c "import sys; print(sys.prefix)"`
    CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:~/anaconda3/envs/testDL/include/python3.6"

    sudo ./bootstrap.sh \
        --with-python-root=$python_root \
        --with-python-version=3.6 \
        --prefix=/usr/include   # installs boost in /usr/include

    sudo ./b2 install
```

2. Clone the repo and compile

```bash
    git XXXX
    cd XXXX
    mkdir build
    cd build
    cmake ..
    make
```

## Run

## Troubleshooting

If a warning appears when running: `....libstdc++.so.6: versionGLIBCXX_3.4.21' not found...` you might need to install `libgcc`

```bash
    conda install libgcc
```

## misc

-   additional information on
    [building python - c++ wrappers with Boost](https://www.preney.ca/paul/archives/107)

-   [Boost](http://www.boost.org/users/history/version_1_64_0.html)

-   [c++ online shell](http://cpp.sh/) or [c++ online compiler](https://rextester.com/l/cpp_online_compiler_gcc)

-   [String search benchmarks](https://almondtools.github.io/stringbench/chart.html#latest)
    from [almondtools github repo](https://github.com/almondtools/stringbench)
