import json
import pytest
from video_indexer.main import VideoIndexer


@pytest.fixture
def mock_video_indexer():
    vi = VideoIndexer('key', 'loc', 'acc_id')
    return vi


def test_get_access_token_success(mocker, mock_video_indexer):
    mock_response = mocker.Mock()
    mock_response.return_value.text = '"some-access-token"'
    mocker.patch('requests.get', mock_response)

    assert mock_video_indexer.get_access_token() == 'some-access-token'


def test_check_access_token_existed(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-token'
    mock_call = mocker.Mock()
    mocker.patch('video_indexer.main.VideoIndexer.get_access_token', mock_call)

    mock_video_indexer.check_access_token()
    assert mock_call.call_count == 0


def test_check_access_token_not_exist(mocker, mock_video_indexer):
    mock_call = mocker.Mock()
    mocker.patch('video_indexer.main.VideoIndexer.get_access_token', mock_call)

    mock_video_indexer.check_access_token()
    assert mock_call.call_count == 1


def test_upload_to_video_indexer_success(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-access-token'
    mock_response = mocker.Mock()
    mock_response.return_value.json.return_value = {
        "accountId": "some-acc-id",
        "id": "some-video-id",
        "name": "temp.mp4",
        "userName": "dummy first name dummy last name",
        "created": "2018-10-05T14:56:34.7268773+00:00",
        "privacyMode": "Private",
        "state": "Processing"
    }
    mocker.patch('requests.post', mock_response)
    mocker.patch('builtins.open')

    video_id = mock_video_indexer.upload_to_video_indexer('in_file', 'candidate_id')

    assert video_id == 'some-video-id'


def test_get_video_info_success(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-access-token'
    mock_response = mocker.Mock()
    mock_response.return_value.json.return_value = {
        'state': 'Processed',
        'accountId': '94b021ec-a0bc-4074-85c6-63d280b328fd',
        'someInfo': 'some info there'
    }
    mocker.patch('requests.get', mock_response)

    video_info = mock_video_indexer.get_video_info('video_id')
    assert video_info == {
        'state': 'Processed',
        'accountId': '94b021ec-a0bc-4074-85c6-63d280b328fd',
        'someInfo': 'some info there'
    }


def test_get_video_info_processing(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-access-token'
    mock_response = mocker.Mock()
    mock_response.return_value.json.return_value = {
        'state': 'Processing',
        'accountId': '94b021ec-a0bc-4074-85c6-63d280b328fd',
        'videos': [{
            'processingProgress': 30
        }],
        'someInfo': 'some info here',
    }

    mocker.patch('requests.get', mock_response)

    video_info = mock_video_indexer.get_video_info('video_id')
    assert video_info == {
        'state': 'Processing',
        'accountId': '94b021ec-a0bc-4074-85c6-63d280b328fd',
        'videos': [{
            'processingProgress': 30
        }],
        'someInfo': 'some info here',
    }


def test_get_caption_from_video_indexer_success(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-access-token'
    mock_response = mocker.Mock()
    mock_response.return_value.content = 'Caption content'
    mocker.patch('requests.get', mock_response)
    content = mock_video_indexer.get_caption_from_video_indexer('video_id')

    assert content == 'Caption content'


def test_get_thumbnail_from_video_indexer_success(mocker, mock_video_indexer):
    mock_video_indexer.access_token = 'some-access-token'
    mock_response = mocker.Mock()
    mock_response.return_value.content = 'Thumbnail content'
    mocker.patch('requests.get', mock_response)
    content = mock_video_indexer.get_thumbnail_from_video_indexer('video_id', 'thumbnail_id')

    assert content == 'Thumbnail content'


def test_extract_summary_from_video_indexer_info(mocker, mock_video_indexer):
    with open('tests/mock_data/video_indexer_output_processed.json') as f:
        info = json.load(f)
        assert mock_video_indexer.extract_summary_from_video_indexer_info(info) == {
            'durationInSeconds': 28,
            'numberOfKeywords': 2,
            'keywords': [
                {
                    "id": 0,
                    "name": "time",
                    "appearances": [
                        {
                            "startTime": "0:00:15.57",
                            "endTime": "0:00:22.8",
                            "startSeconds": 15.6,
                            "endSeconds": 22.8
                        }
                    ],
                    "isTranscript": True
                },
                {
                    "id": 1,
                    "name": "spend",
                    "appearances": [
                        {
                            "startTime": "0:00:01.18",
                            "endTime": "0:00:09.64",
                            "startSeconds": 1.2,
                            "endSeconds": 9.6
                        },
                        {
                            "startTime": "0:00:15.57",
                            "endTime": "0:00:22.8",
                            "startSeconds": 15.6,
                            "endSeconds": 22.8
                        }
                    ],
                    "isTranscript": True
                }
            ],
            'sumOfWordCount': 86,
            'sentimentSeenDurationRatio': {
                'Negative': 0.2286,
                'Neutral': 0.2783,
                'Positive': 0.4735
            },
            'sentimentScore': {
                'Negative': 0.1435,
                'Neutral': 0.6904,
                'Positive': 0.9287
            },
            'transcript': [{
                'confidence': 0.824,
                'text': 'Government spending increasing pressure on banks and other financial '
                'institutions as well as other regulated entities like law firms to know their '
                'customers or effectively know who they were.',
                'textLength': 29,
                'confidencePerText': 23.895999999999997
            }, {
                'confidence': 0.4308,
                'text': 'Play list.',
                'textLength': 2,
                'confidencePerText': 0.8616
            }, {
                'confidence': 0.7806,
                'text': "I'm a lot these companies are doing is poorly as possibly billions, "
                "of dollars in fines if we get.",
                'textLength': 19,
                'confidencePerText': 14.831399999999999
            }, {
                'confidence': 0.8249,
                'text': "Now is the right time to disrupt this market. I 75% of these "
                "organisations feel that they need to spend more time controlling costs around.",
                'textLength': 25,
                'confidencePerText': 20.6225
            }, {
                'confidence': 0.7572,
                'text': "In this moment, we are uniquely positioned to you.",
                'textLength': 9,
                'confidencePerText': 6.8148
            }, {
                'confidence': 0.5722,
                'text': "Helping Dennis.",
                'textLength': 2,
                'confidencePerText': 1.1444
            }]
        }
