import streamlit as st
import requests

API_URL = "http://localhost:8000"

# ── Page Config ────────────────────────────────────────
st.set_page_config(
    page_title="Dev Collaboration Hub",
    page_icon="🚀",
    layout="wide"
)

# ── Session State ──────────────────────────────────────
# Session state is how Streamlit remembers things between interactions
# Like storing your token after login
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# ── Helper Functions ───────────────────────────────────
def get_headers():
    # Returns auth header with token
    return {"Authorization": f"Bearer {st.session_state.token}"}

def is_logged_in():
    return st.session_state.token is not None

# ── Pages ──────────────────────────────────────────────

def show_login_register():
    st.title("🚀 Dev Collaboration Hub")
    st.subheader("Find projects. Build together.")
    st.divider()

    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login Tab
    with tab1:
        st.subheader("Welcome back!")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            if email and password:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.username = email.split("@")[0]
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please fill in all fields")

    # Register Tab
    with tab2:
        st.subheader("Create an account")
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register", use_container_width=True):
            if username and email and password:
                response = requests.post(
                    f"{API_URL}/auth/register",
                    json={
                        "username": username,
                        "email": email,
                        "password": password
                    }
                )
                if response.status_code == 201:
                    st.success("Account created! Please login.")
                elif response.status_code == 400:
                    st.error(response.json()["detail"])
                else:
                    st.error("Something went wrong")
            else:
                st.warning("Please fill in all fields")


def show_projects():
    st.title("🗂️ Projects")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("+ New Project", use_container_width=True):
            st.session_state.page = "create_project"
            st.rerun()

    st.divider()

    # Fetch all projects
    response = requests.get(
        f"{API_URL}/projects/",
        headers=get_headers()
    )

    if response.status_code == 200:
        projects = response.json()

        if not projects:
            st.info("No projects yet. Create the first one!")
        else:
            for project in projects:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.subheader(project["title"])
                        if project["description"]:
                            st.write(project["description"])
                        status = "🟢 Open" if project["is_open"] else "🔴 Closed"
                        st.caption(f"{status} · Owner ID: {project['owner_id']}")
                    with col2:
                        if project.get("github_url"):
                            if st.button("GitHub Stats", key=f"gh_{project['id']}"):
                                st.session_state.selected_project = project
                                st.session_state.page = "github_stats"
                                st.rerun()
    else:
        st.error("Failed to load projects")


def show_create_project():
    st.title("✨ Create New Project")
    st.divider()

    title = st.text_input("Project Title *")
    description = st.text_area("Description")
    github_url = st.text_input("GitHub URL (optional)")
    is_open = st.toggle("Open for collaborators", value=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Project", use_container_width=True):
            if title:
                response = requests.post(
                    f"{API_URL}/projects/",
                    headers=get_headers(),
                    json={
                        "title": title,
                        "description": description,
                        "github_url": github_url if github_url else None,
                        "is_open": is_open
                    }
                )
                if response.status_code == 201:
                    st.success("Project created!")
                    st.session_state.page = "projects"
                    st.rerun()
                else:
                    st.error("Failed to create project")
            else:
                st.warning("Title is required")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.page = "projects"
            st.rerun()


def show_github_stats():
    project = st.session_state.selected_project
    st.title(f"📊 GitHub Stats — {project['title']}")
    st.divider()

    response = requests.get(
        f"{API_URL}/projects/{project['id']}/github",
        headers=get_headers()
    )

    if response.status_code == 200:
        data = response.json()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⭐ Stars", f"{data['stars']:,}")
        with col2:
            st.metric("🍴 Forks", f"{data['forks']:,}")
        with col3:
            st.metric("💻 Language", data['language'] or "N/A")

        st.divider()
        st.subheader(data["name"])
        if data["description"]:
            st.write(data["description"])
        st.caption(f"Last updated: {data['last_updated'][:10]}")
        st.link_button("View on GitHub", data["url"])

    else:
        st.error("Failed to fetch GitHub stats")

    if st.button("← Back to Projects"):
        st.session_state.page = "projects"
        st.rerun()


def show_profile():
    st.title("👤 My Profile")
    st.divider()

    response = requests.get(
        f"{API_URL}/users/me",
        headers=get_headers()
    )

    if response.status_code == 200:
        user = response.json()
        with st.container(border=True):
            st.subheader(f"@{user['username']}")
            st.write(f"📧 {user['email']}")
            status = "✅ Active" if user["is_active"] else "❌ Inactive"
            st.write(f"Status: {status}")
            st.write(f"User ID: {user['id']}")
    else:
        st.error("Failed to load profile")


# ── Navigation ─────────────────────────────────────────

def show_sidebar():
    with st.sidebar:
        st.title("🚀 Dev Collab")
        st.write(f"👋 Hey, {st.session_state.username}!")
        st.divider()

        if st.button("🗂️ Projects", use_container_width=True):
            st.session_state.page = "projects"
            st.rerun()

        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.page = "login"
            st.rerun()


# ── Main App ───────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "login"

if not is_logged_in():
    show_login_register()
else:
    show_sidebar()
    if st.session_state.page == "projects":
        show_projects()
    elif st.session_state.page == "create_project":
        show_create_project()
    elif st.session_state.page == "github_stats":
        show_github_stats()
    elif st.session_state.page == "profile":
        show_profile()
    else:
        show_projects()