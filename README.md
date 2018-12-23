# CCR

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Command line tool for executing programs w/o input test file with 40+ languages support


### Installing

To install the tool from pip

```sh
pip install ccr

```

To install from source
first clone the repo

```
git clone https://github.com/jigarWala/ccr.git
cd ccr
```
Than install the `requirements`

```sh

pip install -r requirements.txt

```
Now install the package by running the following commands

```

python setup.py build
python setup.py install

```

# Usage
  Without using input file
  ``` sh
  ccr test/test.cpp
  
  ```
  
  With using input file
  
  ``` sh
  ccr test/test.py -i test/hello.txt
  ```
  > Note above method uses extension to detect language
  
  Specifying language explicitly
``` sh
  ccr test/test.py -i test/hello.txt -l python3
  ```
# Demo
[![asciicast](https://asciinema.org/a/nkDvjjAQ6d0eMhEUMxPNJj2qU.svg)](https://asciinema.org/a/nkDvjjAQ6d0eMhEUMxPNJj2qU)
# Todo
- [ ] Add more online judge clients
- [ ] better logging
- [ ] better exception handling
- [ ] improve cli

# Note


> For running code on python, preferably use `-l` parameter as python has different version.

> Default is <b>python3</b>, if not specifying `-l`

## Contributing

Please reach out to me if you wish to contribute to this project


## Authors

* **Jigar Wala**  - [jigarWala](https://github.com/jigarWala)

See also the list of [contributors](https://github.com/jigarWala/ccr/contributors) who participated in this project.

## License

This project is licensed under the MIT - see the [LICENSE](./LICENSE) file for details
