from typing import Optional

from markupsafe import Markup


class LinkTag:
    rel: str = None
    href: str = None
    sizes: str = None
    type: str = None
    hreflang: str = None

    _rel: str = None
    _href: str = None
    _sizes: str = None
    _type: str = None
    _hreflang: str = None

    def __init__(
        self,
        rel: str,
        href: Optional[str] = None,
        sizes: Optional[str] = None,
        type_: Optional[str] = None,
        hreflang: Optional[str] = None,
    ):
        self.rel = rel
        self.href = href
        self.sizes = sizes
        self.type = type_
        self.hreflang = hreflang

        self._rel = f'rel="{self.rel}" '
        self._href = f'href="{self.href}" ' if self.href is not None else ""
        self._sizes = f'sizes="{self.sizes}" ' if self.sizes is not None else ""
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._hreflang = (
            f'hreflang="{self.hreflang}" ' if self.hreflang is not None else ""
        )

    def __repr__(self):
        return Markup(
            f"<LinkTag {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
                " >", ">"
            )
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def raw(self):
        return self._compile()

    def _compile(self):
        return f"<link {self._rel}{self._href}{self._sizes}{self._type}{self._hreflang}>".replace(
            " >", ">"
        )


class ScriptTag:
    src: str = None
    type: str = None
    async_: bool = False
    defer: bool = False
    crossorigin: str = None
    integrity: str = None
    nomodule: bool = False
    referrerpolicy: str = None

    _src: str = None
    _type: str = None
    _async: str = None
    _defer: str = None
    _crossorigin: str = None
    _integrity: str = None
    _nomodule: str = None
    _referrerpolicy: str = None

    def __init__(
        self,
        src: str,
        type_: Optional[str] = None,
        async_: bool = False,
        defer: bool = False,
        crossorigin: Optional[str] = None,
        integrity: Optional[str] = None,
        nomodule: bool = False,
        referrerpolicy: Optional[str] = None,
    ):
        self.src = src
        self.type = type_
        self.async_ = async_
        self.defer = defer
        self.crossorigin = crossorigin
        self.integrity = integrity
        self.nomodule = nomodule
        self.referrerpolicy = referrerpolicy

        self._src = f'src="{self.src}" '
        self._type = f'type="{self.type}" ' if self.type is not None else ""
        self._async = f'async="{str(self.async_).lower()}" ' if self.async_ else ""
        self._defer = f"defer " if self.defer else ""
        self._crossorigin = (
            f'crossorigin="{self.crossorigin}" ' if self.crossorigin is not None else ""
        )
        self._integrity = (
            f'integrity="{self.integrity}" ' if self.integrity is not None else ""
        )
        self._nomodule = f"nomodule " if self.nomodule else ""
        self._referrerpolicy = (
            f'referrerpolicy="{self.referrerpolicy}" '
            if self.referrerpolicy is not None
            else ""
        )

    def __repr__(self):
        return Markup(
            (
                f"<ScriptTag {self._src}{self._type}"
                f"{self._async}{self._defer}{self._crossorigin}"
                f"{self._integrity}{self._nomodule}{self._referrerpolicy}>"
            ).replace(" >", ">")
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def raw(self):
        return self._compile()

    def _compile(self):
        return (
            f"<script {self._src}{self._type}"
            f"{self._async}{self._defer}{self._crossorigin}"
            f"{self._integrity}{self._nomodule}{self._referrerpolicy}></script>"
        ).replace(" >", ">")


class BodyContent:
    div_id: str = None
    noscript_message: str = None

    def __init__(
        self,
        div_id: str = "root",
        noscript_message: str = "You need to enable JavaScript to run this app.",
    ):
        self.div_id = div_id
        self.noscript_message = noscript_message

    def __repr__(self):
        return (
            "BodyContent< "
            f"id = {self.div_id} "
            f"noscript = {self.noscript_message} "
            ">"
        )

    def __str__(self):
        return Markup(self._compile())

    def __call__(self, *args, **kwargs):
        return Markup(self._compile())

    def _compile(self):
        return Markup(
            f'<div id="{self.div_id}"></div>\n'
            f"<noscript>{self.noscript_message}</noscript>"
        )
