import requests


class VideoIndexer():
    def __init__(self, vi_subscription_key, vi_location, vi_account_id):
        self.vi_subscription_key = vi_subscription_key
        self.vi_location = vi_location
        self.vi_account_id = vi_account_id
        self.access_token = None

    def get_access_token(self):
        print('Getting video indexer access token...')
        headers = {
            'Ocp-Apim-Subscription-Key': self.vi_subscription_key
        }

        params = {
            'allowEdit': 'true'
        }
        access_token_req = requests.get(
            'https://api.videoindexer.ai/auth/{loc}/Accounts/{acc_id}/AccessToken'.format(
                loc=self.vi_location,
                acc_id=self.vi_account_id
            ),
            params=params,
            headers=headers
        )

        access_token = access_token_req.text[1:-1]
        print('Access Token: {}'.format(access_token))
        self.access_token = access_token
        return access_token

    def check_access_token(self):
        if not self.access_token:
            self.get_access_token()

    def upload_to_video_indexer(self, input_filename, video_name='', video_language='English'):
        self.check_access_token()

        print('Uploading video to video indexer...')
        params = {
            'streamingPreset': 'Default',
            'indexingPreset': 'DefaultWithNoiseReduction',
            'language': video_language,
            'name': video_name,
            'accessToken': self.access_token
        }

        files = {
            'file': open(input_filename, 'rb')
        }

        upload_video_req = requests.post(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos'.format(
                loc=self.vi_location,
                acc_id=self.vi_account_id
            ),
            params=params,
            files=files
        )

        if upload_video_req.status_code != 200:
            print('Error uploading video to video indexer: {}'.format(upload_video_req.json()))
            raise Exception('Error uploading video to video indexer')

        response = upload_video_req.json()
        return response['id']

    def get_video_info(self, video_id, video_language='English'):
        self.check_access_token()

        params = {
            'accessToken': self.access_token,
            'language': video_language
        }
        print('Getting video info for: {}'.format(video_id))

        get_video_info_req = requests.get(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos/{video_id}/Index'.format(
                loc=self.vi_location,
                acc_id=self.vi_account_id,
                video_id=video_id
            ),
            params=params
        )
        response = get_video_info_req.json()

        if response['state'] == 'Processing':
            print('Video still processing, current status: {}'.format(
                response['videos'][0]['processingProgress'],
            ))

        return response

    def get_caption_from_video_indexer(self, video_id, caption_format='vtt', video_language='English'):
        self.check_access_token()

        print('Getting caption from video: {}'.format(video_id))
        params = {
            'accessToken': self.access_token,
            'format': caption_format,
            'language': video_language
        }

        caption_req = requests.get(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos/{video_id}/Captions'.format(
                loc=self.vi_location,
                acc_id=self.vi_account_id,
                video_id=video_id,
            ),
            params=params
        )

        return caption_req.content

    def get_thumbnail_from_video_indexer(self, video_id, thumbnail_id):
        print('Getting thumbnail from video: {}, thumbnail: {}'.format(video_id, thumbnail_id))
        params = {
            'accessToken': self.access_token
        }

        thumbnail_req = requests.get(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos/{video_id}/Thumbnails/{thumbnail_id}'.format(
                loc=self.vi_location,
                acc_id=self.vi_account_id,
                video_id=video_id,
                thumbnail_id=thumbnail_id
            ),
            params=params
        )

        return thumbnail_req.content

    def extract_summary_from_video_indexer_info(self, info):
        return {
            'durationInSeconds': info['durationInSeconds'],
            'numberOfKeywords': len(info['summarizedInsights'].get('keywords', [])),
            'keywords': info['summarizedInsights'].get('keywords', []),
            'sumOfWordCount': sum(info['summarizedInsights']['statistics']['speakerWordCount'].values()),
            'sentimentSeenDurationRatio': {
                x['sentimentKey']: x['seenDurationRatio'] for x in info['summarizedInsights']['sentiments']
            },
            'sentimentScore': {
                x['sentimentType']: x['averageScore'] for x in info['videos'][0]['insights'].get('sentiments', [])
            },
            'transcript': [
                {
                    'confidence': x['confidence'],
                    'text': x['text'],
                    'textLength': len(x['text'].split()),
                    'confidencePerText': x['confidence'] * len(x['text'].split())
                } for x in info['videos'][0]['insights'].get('transcript', [])
            ]
        }
