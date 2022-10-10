from sys import argv
import twitter as tw
import json
import pandas as pd

def shorten_url(input_url, credentials):

    auth = tw.OAuth(
        token=credentials['access_token'],
        token_secret=credentials['access_token_secret'],
        consumer_key=credentials['consumer_key'],
        consumer_secret=credentials['consumer_secret']
    )

    twitter = tw.Twitter(auth=auth)

    if twitter.account.verify_credentials() != {}:
        self_id = twitter.account.verify_credentials()['id_str']

        # If have been link on inbox
        for message in twitter.direct_messages.events.list()['events']:
            url_list = message['message_create']['message_data']['entities']['urls']
            if url_list != []:
                if url_list[0]['expanded_url'] == input_url:
                    return url_list[0]['url']
            else:
                # Create new message
                response_json = twitter.direct_messages.events.new(_json={
                    "event": {
                        "type": "message_create",
                        "message_create": {
                            "target": {
                                "recipient_id": self_id},
                            "message_data": {
                                "text": input_url}}}})

                return response_json['event']['message_create']['message_data']['text']
    else:
        print('Failure credentials!')
        return

if __name__=='__main__':

    # Argv
    if len(argv) == 1:
        input_url = input("Paste link at here: ")
    else:
        input_url = argv[1]
    
    # TODO: Verify link available?

    # Credentials
    if open('credentials.json', 'r'):
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
    else:
        credentials = {}
        credentials['access_token'] = input("access_token")
        credentials['access_token_secret'] = input("access_token_secret")
        credentials['consumer_key'] = input("consumer_key")
        credentials['consumer_secret'] = input("consumer_secret")

    # Get link
    result = shorten_url(input_url, credentials)

    # Output
    pd.DataFrame([result]).to_clipboard(index=False, header=False) # Copy to clipboard
    print(result + " [Copied to clipboard!]") # Print to screen
    input("Press any key to close...")