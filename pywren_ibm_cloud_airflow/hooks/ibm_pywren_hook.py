from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException

import pywren_ibm_cloud


class IBMPyWrenHook(BaseHook):

    def __init__(self, conn_id='ibm_pywren_config'):
        """
        Initializes hook for IBM-PyWren
        """
        # Get config from Airflow's config parameters
        try:
            conn = self.get_connection(conn_id)
            self.pywren_config = conn.extra_dejson
        except AirflowException:
            self.log.warning('Could not find PyWren config in Airflow connections -- Using regular PyWren config file instead')
            self.pywren_config = {}



    def get_conn(self, pywren_executor_config):
        """
        Initializes PyWren IBM-Cloud executor.
        """
        try:
            pywren_executor_config['log_level'] = 'DEBUG'
            pywren_executor_config['config'] = self.pywren_config
            executor = pywren_ibm_cloud.function_executor(**pywren_executor_config)
        except Exception as e:
            log = "Error while getting an executor for IBM Cloud Functions: {}".format(e)
            raise AirflowException(log)
        return executor
