from collections import namedtuple
SongTuple = namedtuple('Song', 'time singer title video singer_url song_url')


class Song(SongTuple):
    __slots__ = ()

    def __str__(self):
        return '{} {} - {}'.format(self.time, self.singer, self.title)

    def __repr__(self):
        return self.__str__()
