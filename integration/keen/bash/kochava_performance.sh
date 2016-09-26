#!/bin/bash


APP_HOME=/opt/dwradiumone/r1-dw-connect-app/dev/kochava_performance
PYTHON=/opt/python2.7/bin/python
SCRIPT_HOME=$APP_HOME/scripts
SCRIPT=integration/keen/real_time/real_time_process.py
ENTITY_NAME=kochava_performance

function log
{
        now="`date +'%Y%m%d %H:%M:%S'`"
        echo $* | sed "s/^/$now:$$:   /"  >> ${APP_HOME}/log/rt/job.log
}

function logerror
{
   log "ERROR: $*"
}

# called by data_triggers framework
export PYTHONPATH="$SCRIPT_HOME"
dt="`date +%Y%m%d`"
hr="`date +%Y%m%d00`"
log "Called from cron, dt = $dt , hr=$hr"
current_date_time="`date +%Y%m%d%H%M%S`"
log "current date time = $current_date_time , dt = $dt, hr = $hr"
process_name=$dt'_'$hr'_'$current_date_time
log "process_name = $process_name"
$PYTHON $SCRIPT_HOME/$SCRIPT $dt $hr $process_name $ENTITY_NAME

exit 0
