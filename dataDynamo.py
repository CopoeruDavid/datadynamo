import boto3
ddb = boto3.client("dynamodb")
import ask_sdk_core
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
sb = SkillBuilder()


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        speech_text = 'Welcome to my Alexa app';
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class ErrorHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speech_text = 'Sorry, your skill encountered an error';
        print(exception)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # any cleanup logic goes here
        return handler_input.response_builder.response

class SilvanaTestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SilvanaTest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Hello Silvana, hope you are doing well";
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response
        

class dataDynamoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("dataDynamoIntent")(handler_input)

    def handle(self, handler_input):
        try:
            data = ddb.get_item(
                TableName="Animals",
                Key={
                    'id': {
                        'S': "1"
                    }
                }
            )
        except BaseException as e:
            print(e)
            raise(e)  
        # slotValue = handler_input.request_envelope.request.intent.slots['slotName'].value
       
        speech_text = "Hello Silvana, your animal is a " + data['Item']['type']['S'];
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response   

class StoreDataHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return is_intent_name("StoreData")(handler_input)

    def handle(self, handler_input):
          
        type = handler_input.request_envelope.request.intent.slots['type'].value
        age = handler_input.request_envelope.request.intent.slots['age'].value
        id = handler_input.request_envelope.request.intent.slots['id'].value
        
        try:
            data = ddb.put_item(
                   TableName="Animals",
                   Item={
                        'id': {
                            'S': id
                        },
                        'type': {
                            'S': type
                        },
                        'age': {
                            'S': age
                        }
                    }
                )
        except BaseException as e:
            print(e)
            raise(e)
        
        
        speech_text = "Thank you for this new addition " + type + age;
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response   

sb.add_exception_handler(ErrorHandler())
#delete undefined built-in intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SessionEndedRequestHandler())
#add custom request handlers
sb.add_request_handler(dataDynamoIntentHandler())
sb.add_request_handler(SilvanaTestHandler())
sb.add_request_handler(StoreDataHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)
