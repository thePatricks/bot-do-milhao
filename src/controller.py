import discord
import quantumrand
import asyncio

from .constants import Lanes

BASE_AUDIO_PATH = "./audios"


class Controller:
    def __init__(self, ctx, *arg):
        self.ctx = ctx
        self.arg = arg

    @property
    def channel_name(self):
        try:
            return self.ctx.author.voice.channel.name
        except AttributeError:
            return "flex do milhao"

    @property
    def lanes(self):
        return [Lanes.TOP, Lanes.JG, Lanes.MID, Lanes.ADC, Lanes.SUP]

    def __random_sort(
        self,
        n: int = 5,
        current: list[Lanes] = [],
        on_hold: list[Lanes] = None,
    ) -> list[Lanes]:
        if on_hold is None:
            on_hold = self.lanes

        if len(on_hold) == 0 or n < 1:
            return current

        if len(on_hold) == 1:
            return [*current, *on_hold]

        picked = quantumrand.list_picker(on_hold)

        current.append(picked)
        on_hold.remove(picked)

        return self.__random_sort(n - 1, current=current, on_hold=on_hold)

    def __get_audio_list(self):
        picks = self.__random_sort()

        current = []

        for lane in self.lanes:
            current.append(f"{BASE_AUDIO_PATH}/{lane.value.lower()}.mp3")
            current.append(f"{BASE_AUDIO_PATH}/{picks.index(lane)+1}.mp3")

        return current

    async def __play_intro(self, vc):
        event = asyncio.Event()
        audio = discord.FFmpegPCMAudio(f"{BASE_AUDIO_PATH}/intro.mp3")
        vc.play(audio, after=lambda _: event.set())
        vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.05)
        await event.wait()

    async def __play(self, vc, audio_list):
        sem = asyncio.Semaphore()

        def after_play(error):
            if error:
                print(f"error playing audios {error}")
            sem.release()

        for audio_source in audio_list:
            await sem.acquire()
            audio = discord.FFmpegPCMAudio(audio_source)
            vc.play(audio, after=after_play)
            vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.05)

        while vc.is_playing():
            pass

    async def run(self):
        try:
            voice_channel = discord.utils.get(
                self.ctx.guild.channels, name=self.channel_name
            )
            vc = await voice_channel.connect()

            [audio_list, _] = await asyncio.gather(
                asyncio.to_thread(self.__get_audio_list), self.__play_intro(vc)
            )

            await self.__play(vc, audio_list)
        finally:
            await vc.disconnect()
