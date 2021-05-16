# import os
# from io import BytesIO
from gtts import gTTS

# from tempfile import NamedTemporaryFile
import pyglet


pyglet.options["audio"] = ("pulse",)

# To play audio text-to-speech during execution


def speak():
    tts = gTTS("so os troll online", lang="pt", tld="com.br")

    filename = "temp.mp3"

    tts.save(filename)

    try:

        sound = pyglet.media.load("./temp.mp3", streaming=False)

        player = sound.play()
        while player.playing:
            pyglet.app.platform_event_loop.dispatch_posted_events()
            pyglet.clock.tick()
    finally:
        pass
        # os.remove(filename)


speak()
