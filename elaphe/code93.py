# coding: utf-8
import re
from bases import Barcode, LinearCodeRenderer, DPI


CODE93_ESCAPE_RE = re.compile(r'\^\d{3}')
CODE93_CHARS ="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%*"
class Code93(Barcode):
    """
    >>> bc = Code93()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Code93 object at ...>
    >>>
    >>> print bc.render_ps_code('THIS IS CODE93') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -12 144 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (THIS IS CODE93) () code93 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('THIS IS CODE93', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'code93'
    aliases = ('code_93', 'code-93', 'code 93')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10)

        def _codelen(self, codestring):
            if self.lookup_option('includecheck', False)==True:
                codelen = len(codestring)+3
            else:
                codelen = len(codestring)+2
            return codelen
            
        def _code_bbox(self, codestring):
            """
            >>> r = Code93._Renderer({})
            >>> r._code_bbox('THIS IS CODE93')
            [0, 0, 144, 72.0]
            """
            return [0, 0, self._codelen(codestring)*9, DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code93._Renderer({})
            >>> r._text_bbox('THIS IS CODE93')
            [0, -12.0, 141.0, 3]
            """
            hidestars = self.lookup_option('hidestars', False)
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            textmaxy = textyoffset + textsize
            textminx = 0
            textmaxx = 9*(len(codestring)+1)+0.6*textsize
            if hidestars:
                textminx, textmaxx = 9, textmaxx-9
            return [0, textyoffset-textsize/2.0, textmaxx, textmaxy]
        
        def build_params(self, codestring):
            params = super(Code93._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params

    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
