import traceback
import json
import time
import boto3


class AWSClient(object):

    def __init__(self, logger):
        self.logger = logger
        self.client = None

    @staticmethod
    def get_thing_reported(client, device_id):
        '''
        :param client:
        :param device_id: string
        :return: dict

        TODO:
        1. use aws sdk to retrieve the shadow of the iot device from aws cloud
        2. retrieve the reported state from the shadow
        '''
        response = client.get_thing_shadow(
            thingName=device_id
        )
        state = response['payload'].read().decode('utf-8')
        response_payload = json.loads(state)
        reported = response_payload['state']['reported']
        return reported

    @staticmethod
    def publish_payload(logger, client, device_id, payload):
        '''
        :param client:
        :param logger:
        :param device_id: string
        :param payload: dict
        :return: boolean

        TODO:
        1. reformat the shadow update topic based on the device id
        2. publish the payload to aws cloud via aws sdk
        3. return True if there is no exception occurs, otherwise, return False
        '''
        topic = f"$aws/things/{device_id}/shadow/update"
        try:
            client.publish(
                topic=topic,
                payload=payload
            )
        except Exception:
            logger.exception(f"{device_id}:Exception while publishing payload")
            traceback.print_exc()
            return False
        return True

    def is_init(self):
        '''
        :return: boolean

        TODO:
        1. initialize aws iot data client
        2. return True if the iot data client is initialized without exceptions, otherwise, return False

        '''
        try:
            self.client = boto3.client("iot-data",
                                       endpoint_url='https://a2dfrytx410fez-ats.iot.us-west-2.amazonaws.com')

        except Exception:
            self.logger.exception("iot data client is not initialized")
            traceback.print_exc()
            self.client = None
            return False
        return True

    def is_connected(self, device_id):
        '''
        :param device_id: string
        :return: boolean

        TODO
        1. get the reported state of the iot device from aws cloud
        2. retrieve the connected state from the reported state
        3. return the connected state or return False if there is any exception occurs
        '''
        try:
            reported_state = self.get_thing_reported(self.client, device_id)
            connected_state = reported_state['connected']
        except Exception:
            self.logger.exception(f"{device_id}: exception occured while retrieving connected state")
            traceback.print_exc()
            return False
        return connected_state

    def update_fan_speed(self, device_id, field, value):
        '''
        :param device_id: string
        :param field: string
        :param  value: integer
        :return: boolean

        TODO:
        1. retrieve the reported state of the iot device from aws cloud
        2. checking if the fan value equals to the desired fan value
        3. generate payload for fan state update if the value is different
        4. publish the payload to aws cloud
        5. wait for 3 seconds
        6. generate payload for fan state update with fan speed zero
        7. publish the payload to aws cloud
        8. return True if there is no exception occurs, otherwise return False
        '''
        try:
            reported = self.get_thing_reported(self.client, device_id)
            response_payload = self.generate_payload(device_id)
            if reported[field] != value:
                response_payload['state']['reported'][field] = value
                self.publish_payload(self.logger, self.client, device_id, response_payload)
            time.sleep(3)
            response_payload['state']['reported'][field] = 0
            self.publish_payload(self.logger, self.client, device_id, response_payload)
        except Exception:
            self.logger.exception(f"{device_id}: Exception occurred while trying to update fan speed ")
            traceback.print_exc()
            return False

        return True

    def generate_payload(self,device_id):
        response = self.client.get_thing_shadow(
            thingName=device_id
        )
        state = response['payload'].read().decode('utf-8')
        response_payload = json.loads(state)
        return response_payload

    def run_client(self, devices, field, value):
        is_init = self.is_init()
        if not is_init:
            self.logger.info('aws client is not initialized')
            return
        for device_id in devices:
            if not self.is_connected(device_id):
                self.logger.info(f'{device_id}: device is disconnected')
                continue
            res = self.update_fan_speed(device_id, field, value)
            self.logger.info(f'update status of {device_id}: {res}')
        self.logger.info('done.')
