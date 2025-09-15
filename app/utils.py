# Create utility functions here.

from app.locales.de import LangDe
from app.locales.en import LangEn

def get_lang(request):
    code = "en"
    if request is not None and hasattr(request, "headers") and request.headers:
        code = request.headers.get("Accept-Language", "en")[:2]
    if code.startswith("de"):
        return LangDe
    return LangEn