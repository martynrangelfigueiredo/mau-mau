"""Tests for internationalization (i18n) module."""
from maumau.i18n import SUPPORTED_LANGUAGES, TRANSLATIONS, t, DEFAULT_LANGUAGE


def test_supported_languages_count():
    assert len(SUPPORTED_LANGUAGES) == 11
    expected_codes = {"pt_BR", "pt_PT", "en", "de", "nl", "pl", "cs", "hu", "es", "fr", "it"}
    assert set(SUPPORTED_LANGUAGES.keys()) == expected_codes


def test_translations_coverage():
    base_keys = set(TRANSLATIONS[DEFAULT_LANGUAGE].keys())
    for code, lang_dict in TRANSLATIONS.items():
        for key in base_keys:
            assert key in lang_dict, f"Missing key '{key}' in language '{code}'"


def test_t_function():
    assert "Start" in t("start_game", "en")
    assert "Iniciar" in t("start_game", "pt_BR")
    assert "Iniciar" in t("start_game", "pt_PT")
    assert "Spiel" in t("start_game", "de")

    # Rules translation test
    assert "Rules" in t("rules", "en")
    assert "Regras" in t("rules", "pt")
    assert "Step 1" in t("rules_content", "en")
    assert "Passo 1" in t("rules_content", "pt")

    # Formatting test
    assert t("round_num", "en", n=3) == "Round 3"
    assert t("round_num", "pt", n=3) == "Rodada 3"

    # Fallback for unknown language
    assert "Start" in t("start_game", "unknown")


def test_pluralize_function():
    from maumau.i18n import pluralize
    assert pluralize(1, "round_sg", "rounds", "pt") == "rodada"
    assert pluralize(2, "round_sg", "rounds", "pt") == "rodadas"
    assert pluralize(1, "game_sg", "games", "pt") == "jogo"
    assert pluralize(3, "game_sg", "games", "pt") == "jogos"

    assert pluralize(1, "round_sg", "rounds", "en") == "round"
    assert pluralize(2, "round_sg", "rounds", "en") == "rounds"
