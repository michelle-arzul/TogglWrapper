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

user = 'YOUR_TOGGL_API_KEY_HERE'
password = 'api_token'
workspace_id = 'YOUR_WORKSPACE_ID_HERE'
DetailedReport.run(user, password, workspace_id)
```
