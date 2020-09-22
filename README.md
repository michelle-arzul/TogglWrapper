# TogglWrapper

A Python wrapper for fetching reports from the Toggl API.

## Requirements

* [Python](https://www.python.org/downloads/) 3.7 or higher.
* [requests](https://pypi.org/project/requests/), use `pip install requests` to install.

## Instructions

Import the relevant class (e.g. DetailedReport) from togglWrapper.py and use its run method.

Press `Ctrl + C` to exit, which will abort fetching.

Example:

```python
from togglWrapper import DetailedReport

if __name__ == '__main__':
    user = '276cba70c2581219b8e9947281c22343'
    password = 'api_token'
    workspace_id = '3923020'
    DetailedReport.run(user, password, workspace_id)
```
