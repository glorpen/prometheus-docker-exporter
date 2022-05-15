import itertools
import textwrap
import typing

T = typing.TypeVar('T')


class Stat:
    _f: typing.Callable
    _metric_class: typing.Type[T]

    def __init__(self, f=None, labels: list = None):
        super(Stat, self).__init__()

        self.labels = labels or []

        if f is not None:
            self(f)

    def __call__(self, f) -> 'Stat':
        self._f = f
        self._metric_class = typing.get_type_hints(f)['metric']
        return self

    @property
    def description(self):
        return textwrap.dedent(self._f.__doc__).replace("\n", " ").strip(" ")

    @property
    def name(self):
        return self._f.__name__

    def update(self, metric: T, data, labels):
        if self.labels:
            self._f(metric=metric, labels=labels, data=data)
        else:
            self._f(metric=metric.labels(**labels), data=data)

    def metric(self, labels: list):
        return self._metric_class(self.name, self.description, self.labels + labels)
