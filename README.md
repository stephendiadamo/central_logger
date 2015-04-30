# Central Logger #

## Setup Instructions ##
* Clone project to a clean directory

```
git clone git@github.com:stephendiadamo/central_logger.git
```

### Server setup ###

* Navigate to server directiory

```
cd central_logger/central_logger_server
```

* Create virtual python environment and install requirements

```
virtualenv venv-server;
source venv-server/bin/activate;
pip install -r requirements.txt;
```

* Run setup script (this only initializes a local database)

```
./setup
```

* Launch server (port 5000)

```
python central_logger_server.py
```


### Client setup ###

* Navigate to client directiory

```
cd central_logger/central_logger_client
```

* Create virtual python environment and install requirements (if in venv-server still, run 'deactivate' first)

```
virtualenv venv-client;
source venv-client/bin/activate;
pip install -r requirements.txt;
```

* Launch client (port 5050)

```
python central_logger_client.py
```

## API ##

### Create a new log entry ###

/logger/api/v1.0/logs

* For adding a new log entry
* Note, new entries are added to a buffer and added to the database ever 15 seconds in bulk
* Entry must include 
  * log_type: The type of log, either error or normal log message
  * event\_type: A specific type of event. Eg. user\_error, server\_error, new\_task, etc.
  * application: The application the log is for. Eg. Todoist, Wedoist, etc. 

* Optional fields are
  * occurred_at: A specific date of the log
  * description: Any additional information  in human readable form
  * log_message: Any error messages or other computer outputs

### Fetch log data ###
/logger/api/v1.0/get_logs

* For fetching log data
* Will return JSON data of all log entries 
* Can filter by 'log_type' by sending an optional parameter 'filter'

### Display data ###

/view_data

* Will render a table view that shows all errors 
* Contains sorting and filtering functionality using jQuery (quite slow for large amounts of data)

## Further Ideas ##

### Filtering and Grouping ###

Within the current project, I have added some jQuery plug-ins that allow for filtering and grouping, but these are slow when there are many logs being displayed. Ideally we will not be viewing every data entry at once. We would like data that has already been aggregated on the server to reduce the amount of data to display. 

I have also allowed users to fetch data based on the log type. This is minimal but it gives the idea of what can be done. Users can query the database for logs from particular dates, event types, and possibly match some regular expressions to find certain exceptions. There are many possibilities. 

I would leave the querying and filtering to the database engine since these are highly developed features, but I would try to use a start and end date for most queries to get only the data that is important to the user and to minimize the amount of data that needs to be handled.

### Removing old logs ###

An easy way to do this would be that every log entry gets deleted after a set time, say thirty days, unless it is flagged as important. We could create a cron-job that runs daily to remove old logs.

