from typing import Any, Callable, Iterable, Literal, Sequence, overload

class EnumType(type):
    def __init__(
        self,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        items: Iterable[tuple[str, Any, str | None, bool]],
    ) -> None: ...
    def _create(
        self, name: str, value: int, doc: str | None = None, by_value_only: bool = False
    ) -> None: ...
    def __len__(self) -> None: ...
    def __iter__(self) -> None: ...
    def __getitem__(self, key: str | int | EnumType) -> None: ...
    def _get(self, value: int, create: bool = False) -> None: ...
    def _get_multi_flags(self, value: int) -> None: ...
    def get(
        self,
        key: str | int | EnumType,
        default: int | None = None,
        create: bool = False,
    ) -> int | None: ...

class EnumItem:
    name: str
    value: int

    def __int__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __reduce__(self) -> tuple[Callable[[str, str, str], EnumItem], tuple[str, str, str]]: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class EnumFlag(EnumItem):
    flags: tuple[EnumFlag]

    def __and__(self, other: object) -> EnumFlag: ...
    def __or__(self, other: object) -> EnumFlag: ...
    def __xor__(self, other: object) -> EnumFlag: ...
    def __invert__(self) -> bool: ...
    def __nonzero__(self) -> bool: ...

@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: Literal[True],
) -> EnumFlag: ...
@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: Literal[False],
) -> EnumItem: ...
@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: bool = False,
) -> EnumItem | EnumFlag: ...
