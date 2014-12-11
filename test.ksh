#!/bin/ksh

######################################################################
# Script : d_byr_ld.ksh
# Description : This script loads the company table DWH_D_BYR_LU
#               using SOURCE TABLE BUYER_ASGN JOINED WITH DWH_D_EMP_LU.
# Modifications
# 1/7/2013  : Yomari  : Initial Script
######################################################################


export SCRIPT_NAME=$(basename ${0%%.ksh})

export HOME=/express

export ETLHOME=${HOME}/scripts

. ${ETLHOME}/etc/ENV.cfg

export DIM_CLOSABLE=1

. ${LIB_DIR}/run_lib.ksh

##################################################

SOURCE_TABLE="BUYER_ASGN"
TARGET_TABLE="DWH_D_BYR_LU"
TEMP_TABLE="TMP_${TARGET_TABLE#DWH_}"

DIM_IDNT='BYR_ID'
DIM_KEY='BYR_KEY'

TEMP_TABLE_COLUMN='EMP_KEY
BYR_NAME
BYR_PHONE_NUM
BYR_FAX'

####### SET VARIABLES ######################################

set_variables

print_msg "$SCRIPT_NAME Started"
start_script
####### LOAD INTO TEMPORARY TABLE ##########################

print_msg "Load into Temporary Table Started"

print_msg "Truncate Temporary Table"

truncate_table -d "${TEMP_DB}" -t "${TEMP_TABLE}"

print_msg "${TEMP_TABLE} truncated successfully"

print_msg "Loading ${TEMP_TABLE}"

INSERT_SQL="INSERT INTO ${TEMP_DB}..${TEMP_TABLE}
            ( ${DIM_IDNT}
             ,${TEMP_TABLE_COLUMN_LIST}
             )
           SELECT EMP_INIT
                  ,EMP_KEY
                  ,FIRST_NAME || ' ' || DECODE(MIDDLE_NAME, NULL, '', MIDDLE_NAME || ' ') || LAST_NAME
                  ,PHONE_NUM BYR_PHONE_NUM
                  ,NULL BYR_FAX
               FROM ${TARGET_DB}..DWH_D_EMP_LU WHERE (EMP_INIT) IN (SELECT DISTINCT(EMP_INIT_BUY) FROM ${SRC_DB}..${SOURCE_TABLE})"
               
run_query -d "$TEMP_DB" -q "$INSERT_SQL" -m "Unable to Insert Records for the Buyer into temp table" 

print_msg "${TEMP_TABLE} loaded successfully"

############### TEMPORARY TABLE LOAD COMPLETE ########################

print_msg "Loading $TARGET_TABLE"

close_using_temp

update_using_temp

reopen_using_temp

insert_from_temp

print_msg "$TARGET_TABLE Load Complete"

script_successful
