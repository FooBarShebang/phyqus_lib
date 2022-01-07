# phyqus_lib

Python 3 implementation of the 'real life measurements', i.e. 2-tuple values of the most probale / mean value and the asssociated uncertainty / standard error, which can be generic or specific type (i.e. with the associated 'dimension' / physical quantity like meters, gramms, amperes, etc.). Also implements the 'typed' arithmetic, e.g. one can multiply and divide meters and seconds but not add or subtract, whereas addition and subtraction are allowed for the same quantities (meters and miles, for instance). The library name is a contraction of **phy**sical **qu**antitie**s**.

## Installation

Clone the official repository into your local workspace / project folder:

```bash
$git clone <repository_path> "your projects folder"/phyqus_lib
```

Check the system requirements and dependencies:

```bash
$cd "your projects folder"/phyqus_lib
$python3 ./check_dependencies.py
```

### For developers only

Initialize the UML templates submodule

```bash
$cd "your projects folder"/phyqus_lib/Documents/UML/Templates
$git submodule init
```

Download the content of the UML templates submodule

```bash
$git submodule update --recursive --remote
```

## System requirements

This library is written in Python 3 programming language (>= v3.6) and is intended to be OS platform independent. At least, it is tested under MS Windows and GNU Linux OSes, see [Documents/Tests/tested_OS.md](./Documents/Tests/tested_OS.md).

This library depends on additional Python packages, which should be installed as well (see [Dependencies.md](./Dependencies.md)).

## Documentation

* [Design](./Documents/Design/index.md)
* [Requirements](./Documents/Requirements/index.md)
* [Test reports](./Documents/Tests/index.md)
* [User and API references](./Documents/References/index.md)
