import secrets as _secrets
from urllib.parse import urlencode

import requests
import streamlit as st

_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
_TOKEN_URL = "https://oauth2.googleapis.com/token"
_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
_SCOPES = "openid email profile"


def _cfg():
    missing = [k for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "REDIRECT_URI") if k not in st.secrets]
    if missing:
        st.error(f"Secrets ausentes no Streamlit Cloud: {', '.join(missing)}\nConfigure em Settings → Secrets.")
        st.stop()
    return {
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": st.secrets["REDIRECT_URI"],
        "allowed_domain": st.secrets.get("ALLOWED_DOMAIN", "suzano.com.br"),
    }


def _build_auth_url() -> str:
    cfg = _cfg()
    params = {
        "client_id": cfg["client_id"],
        "redirect_uri": cfg["redirect_uri"],
        "response_type": "code",
        "scope": _SCOPES,
        "prompt": "select_account",
        "access_type": "offline",
    }
    return f"{_AUTH_URL}?{urlencode(params)}"


def _exchange_code(code: str) -> dict:
    cfg = _cfg()
    resp = requests.post(
        _TOKEN_URL,
        data={
            "code": code,
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "redirect_uri": cfg["redirect_uri"],
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def _get_user_info(access_token: str) -> dict:
    resp = requests.get(
        _USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def require_auth() -> dict:
    """
    Insira no topo do app.py:  user = require_auth()
    Retorna o dicionário do usuário se autenticado,
    caso contrário exibe a tela de login e para a execução.
    """
    # Já autenticado nesta sessão
    if "user" in st.session_state:
        return st.session_state["user"]

    # Callback do Google — code na URL
    qp = st.query_params
    if "code" in qp:
        with st.spinner("Autenticando..."):
            try:
                token_data = _exchange_code(qp["code"])
                user_info = _get_user_info(token_data["access_token"])
            except Exception as exc:
                st.error(f"Erro ao autenticar com Google: {exc}")
                st.query_params.clear()
                st.stop()

        email: str = user_info.get("email", "")
        allowed = _cfg()["allowed_domain"]

        if not email.lower().endswith(f"@{allowed}"):
            st.error(f"Acesso negado. Apenas contas @{allowed} podem acessar este sistema.")
            st.query_params.clear()
            st.stop()

        st.session_state["user"] = {
            "name": user_info.get("name", ""),
            "email": email,
            "picture": user_info.get("picture", ""),
        }
        st.query_params.clear()
        st.rerun()

    # Tela de login
    _render_login()
    st.stop()


def logout():
    st.session_state.pop("user", None)
    st.rerun()


def _render_login():
    st.markdown(
        """
        <style>
        section[data-testid="stAppViewContainer"] > div:first-child {
            padding-top: 5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("### Equalização de Fornecedores — MCC")
        st.markdown("Faça login com sua conta Suzano para continuar.")
        st.markdown("")
        auth_url = _build_auth_url()
        st.link_button(
            "Entrar com Google",
            auth_url,
            use_container_width=True,
            type="primary",
        )
