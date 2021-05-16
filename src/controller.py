import discord
import quantumrand
import asyncio
import time

from .constants import Lanes

BASE_AUDIO_PATH = "./audios"


class Controller:
    def __init__(self, ctx, *arg):
        self.ctx = ctx
        self.arg = arg
        self.sem = asyncio.Semaphore()

    @property
    def channel_name(self):
        # TODO: Generalizar channel_name com base no self.ctx
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
        start_time = time.time()

        # TODO: Otimizar essa chamada para que ela ocorra
        # enquanto a musica de intro está tocando
        picks = self.__random_sort()

        current = [f"{BASE_AUDIO_PATH}/intro.mp3"]

        for lane in self.lanes:
            current.append(f"{BASE_AUDIO_PATH}/{lane.value.lower()}.mp3")
            current.append(f"{BASE_AUDIO_PATH}/{picks.index(lane)+1}.m4a")

        print("--- %s seconds ---" % (time.time() - start_time))
        return current

    async def connect_voice_channel(self):
        voice_channel = discord.utils.get(
            self.ctx.guild.channels, name=self.channel_name
        )
        vc = await voice_channel.connect()
        return vc

    def after_play(self, error):
        print(f"error {error}")
        self.sem.release()

    async def play(self):
        vc = await self.connect_voice_channel()

        for audio_source in self.__get_audio_list():
            await self.sem.acquire()
            audio = discord.FFmpegPCMAudio(audio_source)
            vc.play(audio, after=self.after_play)
            vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.05)

        while vc.is_playing():
            pass

        await vc.disconnect()
