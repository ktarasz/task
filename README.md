### GithubWebSearch
[![Build Status](https://travis-ci.org/ktarasz/task.svg?branch=master)](https://travis-ci.org/ktarasz/task)

GitHub web crawler based on the GitHub search

```python
from crawler import GithubWebSearch

GithubWebSearch(
    keywords, 
    object_type,
    extra,
    proxies
)

for batch in crawler_instance:
    somejob(batch)
```
#### Arguments
* **keywords**

    List of keywords to be used as search terms

* **object_type**

    The type of object we are searching for
    * Repositories
    * Issues
    * Wikis

* **extra**

    Enable collect extra artifacts for Repositories. Enabled by default.

* **proxies**

    List of proxies

#### Instalation
Install with pip into python (virtual environment) extra `requrements.txt`:
```bash
$ virtualenv -p python3 venv
...
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Examples
##### Case 1
Python code
```python
from crawler import GithubWebSearch
from pprint import pprint
crawler_instance = GithubWebSearch(
    ('openstack', 'nova', 'css'), 'Repositories', 
    extra=False
)
for batch in crawler_instance:
    pprint(batch)
```
Output
```python
[{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'},
 {'url': 'https://github.com/michealbalogun/Horizon-dashboard'}]
```
##### Case 2
Python code
```python
from crawler import GithubWebSearch
from pprint import pprint
crawler_instance = GithubWebSearch(
    ('openstack', 'nova', 'css'), 'Repositories', 
    extra=True
)
for batch in crawler_instance:
    pprint(batch)

```
Output
```bash
[{'extra': {'language_stats': {'CSS': 52.0, 'HTML': 0.8, 'JavaScript': 47.2},
            'owner': 'atuldjadhav'},
  'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'},
 {'extra': {'language_stats': {'Python': 100.0}, 'owner': 'michealbalogun'},
  'url': 'https://github.com/michealbalogun/Horizon-dashboard'}]
```

### Tests
```bash
$ pytest --cov=crawler --cov-report term-missing 
=================================== test session starts ===================================
platform linux -- Python 3.7.4, pytest-5.2.4, py-1.8.0, pluggy-0.13.0
rootdir: ****
plugins: requests-mock-1.7.0, cov-2.8.1
collected 4 items                                                                         

test/test_crawler.py ....                                                           [100%]

----------- coverage: platform linux, python 3.7.4-final-0 -----------
Name         Stmts   Miss  Cover   Missing
------------------------------------------
crawler.py      49      1    98%   80


==================================== 4 passed in 0.19s ====================================
```
