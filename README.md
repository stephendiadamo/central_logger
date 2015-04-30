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

* Create virtual python environment and install requirements

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



