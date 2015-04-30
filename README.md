# Central Logger #

## API ##

### Create a new log entry ###

/logger/api/v1.0/logs

* For adding a new log entry
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
* Will return JSON data of log entries 
* Can filter by 'log_type' by sending an optional parameter 'filter'
