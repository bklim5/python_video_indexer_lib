# video_indexer

This library provides some common function for operating with Microsoft Video Indexer API

### Getting started
```
pip install video_indexer
```

### Create a VideoIndexer instance
```
from video_indexer import VideoIndexer

CONFIG = {
    'SUBSCRIPTION_KEY': '',
    'LOCATION': '',
    'ACCOUNT_ID': ''
}

vi = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)
```
where
SUBSCRIPTION_KEY can be found at https://api-portal.videoindexer.ai/developer
LOCATION & ACCOUNT_ID can be found at https://www.videoindexer.ai/settings/account

### Upload a video for indexing
```
video_id = vi.upload_to_video_indexer(
   input_filename='some-video.mp4',
   video_name='some-video-name',  # identifier for video in Video Indexer platform, must be unique during indexing time
   video_language='English'
)
```
The library will retry with delay if it's being hit by throttling limit. Maximum 5 times of retrying.

### Get information for a video
```
info = vi.get_video_info(
    video_id,
    video_language='English'
)
```