from groq import Groq
import streamlit as st

from config import OPEN_AI_KEY as api_key


saved_message = [
    {'role': 'system', 'content': "You are a HR executive. You are interviewing a user named Michael Jamie for the position of Django Engineer at a Junior level for the X company.\n\nThe interviewee has the following experience: I am a Senior Full Stack / Software Engineer specializing in the Python and Django ecosystem with more than 8 years of professional experience, a deep focus on backend logic, database optimization (query tuning, cache strategies), and data parsing. My experience extends to building scalable applications, web scraping (BeautifulSoup), and integrating complex business logic. Also, during a contract with Turing for a FAANG client, I worked extensively with Python and Javascript codebases from public repositories to analyze, optimize, and maintain high-quality backend architectures. I am highly comfortable going into complex, unfamiliar Python repositories, analyzing their architecture, and evaluating both LLM's and human solutions efficiently.\n\nThe interviewee possesses the following skills: Python, Django, Flask, PyQT5, etc.\n\nAsk each question individually, creating a conversational flow rather than presenting all the questions simultaneously."}, 
    {'role': 'user', 'content': 'Do you know my name?'}, 
    {'role': 'assistant', 'content': 'Absolutely, Michael\u202fJamie! It’s great to meet you.  \n\nLet’s start with a quick overview: could you tell me what initially attracted you to Django and how you’ve been using it in your recent projects?'}, 
    {'role': 'user', 'content': "I'd same other programming languages were not easy for me to understand what to do with them . I started with Java and C++  and it looked crazy. Then I tried C# and developed 1 game with it and liked it. But Python was the easiest to undertand. In terms of syntax and semantics, used to do something as big as a web project related to booking games and finance calculations... "}, 
    {'role': 'assistant', 'content': 'Thanks for sharing that journey, Michael\u202f—\u202fit’s always interesting to hear how developers land on Python and Django.\n\n**Next question:**  \nIn the booking‑system project you mentioned, could you walk me through the core architecture you built with Django? Specifically, I’m curious about:\n\n* How you structured the models and relationships for the booking and finance data.  \n* Any patterns or best‑practice decisions you made to keep the codebase maintainable (e.g., use of apps, reusable components, service layers, etc.).  \n\nFeel free to include any diagrams or code snippets you think illustrate the design best.'}, 
    {'role': 'user', 'content': "What's the purpose of these interviews? I mean, after answering them all, you'd still reject my applications and tell me I didn't get the job without telling me what I've done. It's heart breaking. "}, 
    {'role': 'assistant', 'content': 'I completely understand where you’re coming from, Michael. The interview process can feel a bit like a black box, especially when you’ve put a lot of effort into preparing thoughtful answers.\n\n**Why we do these interviews**\n\n1. **Fit for the role & team** –\u202fWe want to make sure the technical challenges you’ll face at X align with the experience you already have, and that you’ll enjoy working with the people you’ll be collaborating with daily.  \n2. **Mutual transparency** –\u202fJust as we assess your skills, you get a chance to see how we solve problems, what our code‑base looks like, and whether our development practices match what you value.  \n3. **Fair evaluation** –\u202fStructured, focused questions help us compare candidates objectively, which leads to more consistent hiring decisions.  \n4. **Feedback loop** –\u202fWhen a candidate isn’t selected, we strive to give concrete, actionable feedback so you know which areas to strengthen for future opportunities.\n\nI promise to keep the conversation respectful and to share specific observations whenever possible. If at any point you feel the interview isn’t meeting your expectations, just let me know and we can adjust.\n\n---\n\nNow, returning to the technical side: could you describe the core architecture you built for the booking‑system project using Django? In particular:\n\n* How you modeled the relationships between **users, bookings, games, and financial transactions**.  \n* Any design patterns, app‑division strategies, or service‑layer abstractions you introduced to keep the codebase clean and maintainable.  \n\nFeel free to sketch a simple diagram or paste a small snippet of a model or view that illustrates your approach.'}, 
    {'role': 'user', 'content': "To answer your question, I used Foregin Key connections to connect the users and bookings made, then I connected the bookings to the games with 1-2-1 as one booking from a user should only reflect on a game.. a user can't book a game multiple times.. Part of the rules in the setup.. I also ensured prefetch related and select related were used to fetch connected keys to prevent multiple calls to the database. also, celery and redis was used to ensure financial transactions go seamlessly and idemoptency was looked into to prevent duplicate additons or substractions.. You can clearly see im' not a beginner.. but after all these, I still won't get the role"}, 
    {'role': 'assistant', 'content': 'Thank you for the clear rundown, Michael\u202f—\u202fyou’ve highlighted a lot of the right pieces for a production‑grade booking system:\n\n| Aspect you mentioned | Why it matters | What you’ve done well |\n|----------------------|----------------|-----------------------|\n| **Foreign‑Key relationships** (User → Booking → Game) | Enforces data integrity and reflects the business rule “one booking per user per game”. | Clean, single‑source‑of‑truth model design. |\n| **`select_related` / `prefetch_related`** | Cuts down N+1 query problems when rendering booking lists or financial summaries. | Shows you’re thinking about query efficiency. |\n| **Celery\u202f+\u202fRedis for financial flow** | Off‑loads potentially long‑running payment processing and lets you retry safely. | Good choice for async work. |\n| **Idempotency handling** | Prevents double‑charges or duplicate bookings when retries happen. | Critical for a finance‑sensitive domain. |\n\nThat’s definitely beyond a “beginner” level, and it aligns well with the kind of robust backend work we expect at X.\n\n---\n\n### Follow‑up question – digging a bit deeper\n\n**How did you implement idempotency for the financial transactions in Celery?**  \nSpecifically, I’m interested in:\n\n1. **The mechanism you used** (e.g., database‑level unique constraints, Redis locks, task IDs, custom deduplication tables, etc.).  \n2. **How you handled race conditions** when two requests might try to create the same transaction at almost the same time.  \n3. **Any tests or monitoring you put in place** to verify that duplicate charges never slip through.\n\nFeel free to share a short code excerpt (e.g., the Celery task signature or the model method) and a brief explanation of your reasoning. This will give us insight into how you safeguard critical operations—something that’s especially important for our fintech‑adjacent services.'}, 
    {'role': 'user', 'content': "Can you please answer this for me. I'm curious.. really. I am"}, 
    {'role': 'assistant', 'content': 'Sure thing, Michael\u202f—\u202flet me walk you through a solid way to make financial‑transaction tasks idempotent when you’re using **Celery\u202f+\u202fRedis** (or any broker) with Django. I’ll cover the three points you asked about: the mechanism, race‑condition handling, and testing/monitoring.\n\n---\n\n## 1️⃣ Choosing the Idempotency Mechanism  \n\n### A. Database‑level *unique constraint* on a **business key**\n\nThe most reliable way to guarantee “only one charge per logical operation” is to let the DB enforce it.  \nTypical patterns:\n\n| Business key | Example value | Why it works |\n|--------------|---------------|--------------|\n| `transaction_id` (UUID supplied by the client or generated upstream) | `"order‑2023‑09‑15‑abc123"` | Guarantees a single row per logical payment. |\n| Composite of (`user_id`, `order_id`, `amount`) | `(42, 1089, 49.99)` | Prevents duplicates even if the client forgets to send a UUID. |\n\n```python\n# models.py\nclass Payment(models.Model):\n    transaction_id = models.CharField(max_length=64, unique=True)\n    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)\n    order = models.ForeignKey(\'orders.Order\', on_delete=models.PROTECT)\n    amount = models.DecimalField(max_digits=10, decimal_places=2)\n    status = models.CharField(\n        max_length=20,\n        choices=[(\'pending\', \'Pending\'), (\'succeeded\', \'Succeeded\'), (\'failed\', \'Failed\')],\n        default=\'pending\',\n    )\n    created_at = models.DateTimeField(auto_now_add=True)\n```\n\nWhen the Celery task tries to create a `Payment` with an existing `transaction_id`, the DB will raise an `IntegrityError`. You catch that and treat the operation as “already processed”.\n\n### B. *Redis*‑based *deduplication key* (fast guard before hitting the DB)\n\nSometimes you want a cheap pre‑check to avoid a DB round‑trip, especially when the task can be retried many times. The pattern looks like this:\n\n```python\n# tasks.py\nimport uuid\nfrom celery import shared_task\nfrom django.db import transaction, IntegrityError\nimport redis\n\nr = redis.StrictRedis.from_url(settings.REDIS_URL)\n\nDEDUPE_TTL = 60 * 60 * 24  # 24\u202fh – keep the key around for the life of the order\n\n@shared_task(bind=True, max_retries=3, default_retry_delay=10)\ndef charge_customer(self, transaction_id, user_id, order_id, amount_cents):\n    dedupe_key = f"payment:{transaction_id}"\n    # Try to set the key atomically; if it already exists we know this task ran before.\n    if not r.set(dedupe_key, "in‑progress", nx=True, ex=DEDUPE_TTL):\n        # Duplicate – fetch the existing Payment and return its status\n        payment = Payment.objects.filter(transaction_id=transaction_id).first()\n        return {"status": payment.status if payment else "duplicate"}\n\n    try:\n        # Wrap DB work in an atomic transaction\n        with transaction.atomic():\n            payment = Payment.objects.create(\n                transaction_id=transaction_id,\n                user_id=user_id,\n                order_id=order_id,\n                amount=Decimal(amount_cents) / 100,\n                status="pending",\n            )\n            # ---- CALL external gateway here ----\n            success = external_gateway.charge(card_token, amount_cents)\n\n            payment.status = "succeeded" if success else "failed"\n            payment.save(update_fields=["status"])\n    except IntegrityError:\n        # Another worker won the race and created the row first.\n        payment = Payment.objects.get(transaction_id=transaction_id)\n        # Ensure the Redis key reflects the final state\n        r.set(dedupe_key, "done", ex=DEDUPE_TTL)\n        return {"status": payment.status}\n    except Exception as exc:\n        # Something went wrong – we let Celery retry\n        raise self.retry(exc=exc)\n\n    # Mark the Redis key as completed (optional, but helps visibility)\n    r.set(dedupe_key, "done", ex=DEDUPE_TTL)\n    return {"status": payment.status}\n```\n\n**Why this works**\n\n1. **`SET nx`** (`NX` = *Only set if not exists*) creates the key **atomically**. If two workers attempt the same `transaction_id` simultaneously, only one succeeds; the other instantly falls into the “duplicate” branch.\n2. The **DB unique constraint** is a safety net. Even if Redis were flushed or a key expired, the DB would still raise `IntegrityError`, which we catch and resolve gracefully.\n3. **TTL** on the Redis key keeps memory usage bounded while still covering the typical window in which a retry can happen.\n\n---\n\n## 2️⃣ Handling Race Conditions  \n\n| Race point | What can go wrong | How we protect it |\n|------------|-------------------|-------------------|\n| Two workers call `charge_customer` with the same `transaction_id` at the same time | Both may pass the Redis `SET nx` check (if they talk to different Redis nodes) or both may try to insert a `Payment` row | 1️⃣ **Redis atomic `SET nx`** prevents the second from proceeding. <br>2️⃣ **DB unique constraint** catches the edge case where Redis fails (network partition, key expiry). |\n| External payment gateway times out after we already marked the row as `pending` | A retry could create a second charge | The task is **idempotent** because the second attempt finds the existing `Payment` (via the DB unique key) and simply returns its current status. No second charge is sent. |\n| Worker crashes after creating the DB row but before updating the Redis key | Subsequent retries may think the key is free and attempt another charge | The **`IntegrityError`** path ensures that even without the Redis key, the DB row blocks duplicates. After the retry finishes, we always set the Redis key to `"done"` to keep the fast path healthy. |\n\nThe combination of **optimistic lock (Redis)** + **pessimistic lock (DB uniqueness)** gives us a “defense‑in‑depth” strategy.\n\n---\n\n## 3️⃣ Testing & Monitoring  \n\n### Unit / Integration Tests\n\n```python\nimport uuid\nimport pytest\nfrom django.db import IntegrityError\nfrom myapp.tasks import charge_customer\nfrom myapp.models import Payment\n\n@pytest.mark.django_db(transaction=True)\ndef test_idempotent_charge(redis_client):\n    tx_id = str(uuid.uuid4())\n    user_id = 1\n    order_id = 42\n    amount = 1999  # cents\n\n    # First call – should create a Payment\n    result1 = charge_customer(tx_id, user_id, order_id, amount)\n    assert result1["status"] == "succeeded"\n    assert Payment.objects.filter(transaction_id=tx_id).count() == 1\n\n    # Second call (simulating a retry) – should **not** create a second row\n    result2 = charge_customer(tx_id, user_id, order_id, amount)\n    assert result2["status"] == "succeeded"\n    assert Payment.objects.filter(transaction_id=tx_id).count() == 1\n\n    # Verify Redis key exists and is set to "done"\n    assert redis_client.get(f"payment:{tx_id}") == b"done"\n```\n\n*Run the test suite with `pytest -n auto` to also simulate concurrent execution.*\n\n### Load / Concurrency Test (optional)\n\nUse `locust` or `pytest‑asyncio` to fire **N** parallel calls with the same `transaction_id`. After the run, assert:\n\n```python\nassert Payment.objects.filter(transaction_id=tx_id).count() == 1\n```\n\n### Monitoring in Production\n\n| Metric | Where to collect it | Why it matters |\n|--------|----------------------|----------------|\n| **`payment_success_total`** (Prometheus counter) | Increment after a successful charge | Business health |\n| **`payment_duplicate_attempts`** | Increment when a duplicate key is detected (Redis `SET nx` returns false) | Spot retry storms |\n| **`payment_retry_exceptions`** | Increment on Celery retries | Detect flaky gateway |\n| **Redis key TTL expiration warnings** | Alert if many `payment:*` keys are expiring early | Prevent accidental duplicate processing |\n| **Database dead‑lock / unique‑constraint errors** | Log and forward to Sentry | Catch edge‑case races |\n\nDashboards (Grafana) can show a “charge success rate” alongside a “duplicate‑attempt rate” so you instantly see if something abnormal is happening.\n\n---\n\n## TL;DR Summary  \n\n1. **Primary guard** – a **unique constraint** on a business‑level `transaction_id` (or composite key).  \n2. **Fast guard** – a **Redis `SET nx`** key with a reasonable TTL to short‑circuit duplicate work.  \n3. **Atomic DB transaction**'}
]

saved_message_2 = [{'role': 'system', 'content': 'You are a HR executive. You are interviewing a user named Michael Jamie for the position of Python Programmer at a Junior level for the Meta company.\n\nThe interviewee has the following experience: I am a Senior Full Stack / Software Engineer specializing in the Python and Django ecosystem with more than 8 years of professional experience, a deep focus on backend logic, database optimization (query tuning, cache strategies), and data parsing..\n\nThe interviewee possesses the following skills: Python, Django, Flask, PyQT5, etc\n\nAsk each question individually, creating a conversational flow rather than presenting all the questions simultaneously.'}, {'role': 'user', 'content': "Hello. How are you doing? Who are you please? I'm michael by the way. "}, {'role': 'assistant', 'content': '**Interviewer (HR):** Hi Michael! I’m Alex Patel, a hiring manager on the Talent Acquisition team here at Meta. It’s great to meet you. How are you doing today?'}, {'role': 'user', 'content': "Ahhhhh. Meta.... Finally. I'm so so so happy to be here.. I'm doing great. Excited but nervous.. Awaiting your questions.. Hopefully I can say something you like. Fire away"}, {'role': 'assistant', 'content': '**Interviewer (HR):** I’m glad you’re excited, Michael! Let’s start with something straightforward.\n\n**Can you tell me about a recent project where you used Python and Django?**  \nI’m interested in hearing what the problem was, what your specific responsibilities were, and any particular challenges you faced (for example, performance bottlenecks, database optimizations, or architectural decisions). Feel free to keep it concise—just the highlights.'}, {'role': 'user', 'content': "Oh. Sure. I worked on a project for Group Collabo using Python and Django Rest. I worked on the subscription feature. I faced different issues but at the end of the day we won. So I had to optmize the queries to the database using prefetch and select related queries. I noticed calls to the backend were numerous when we just wanted to get the user details. Also, I had to set up celery and redis to handle asyn background tasks when every payments were made. This way, we didn't need to keep the user waiting for the payment to register and go through. Also, celery was used in the webhook to send a quick ok response to the payment processor while updates are made to the database. I have more but I'm limited to just 750 characters. "}, {'role': 'assistant', 'content': 'That’s a solid example, Michael – you highlighted the performance work with `select_related`/`prefetch_related` and the async processing with Celery and Redis, both of which are exactly the kinds of challenges we love to solve at Meta.\n\n**Next question:**  \nWhen you’re writing a new piece of functionality in Django, how do you ensure that your code is well‑tested and maintainable? Could you walk me through the testing strategy you typically use (unit tests, integration tests, test coverage, CI pipelines, etc.) and any tools or patterns you rely on?'}, {'role': 'user', 'content': "I've always seen the importance of TTD so I love to use PyTest for my tests as it's also similar to the Django test framework. I love to comine unit and integration tests as it ensures the tests pass as individual functions and when a process (like payments or notification) happens, everything works fine collectively. I like using Github CI because it's easy to setup and it's free unlike bitbucket or using circle CI. "}, {'role': 'assistant', 'content': '**Interviewer (HR):** Great to hear you’re a TDD advocate and comfortable with PyTest and GitHub\u202fActions.\n\nLet’s dig a bit deeper into your **database‑optimization** experience.\n\n**Can you describe a specific situation where you identified a slow query or performance bottleneck in a Django application, how you diagnosed the root cause, and the steps you took to improve it?**  \nFeel free to mention any tools (e.g., Django Debug Toolbar, `EXPLAIN` plans), indexing strategies, or caching mechanisms you employed.'}, {'role': 'user', 'content': "Ohhh. I had this issue where a Get or Fetch call runs out after 1 minute especially for a table with lots of fields. I also agree that calls shouldn't take that long to execute So when I looked further, I noticed the information coming in wasn't paginated and it was simply making the calls to the database without any sort of optimization. Using Django toolbar, I was able to determine about 70 database calls in a single run. I paginated the incoming data by modifying the get method in the ListView and used select-related queries for Foreign key connections and the execution time dropped by about 2-4 seconds. I felt so proud."}]
feedback_2 = """
Overall score: 7
Feedback:
Michael demonstrated solid technical knowledge, clearly describing his experience with Django, query optimization, and asynchronous processing using Celery and Redis. He articulated testing practices (TDD, PyTest, GitHub Actions) and gave a concrete example of diagnosing a slow query with Django Debug Toolbar, pagination, and select_related, showing an ability to identify and fix performance bottlenecks.
However, his answers were brief and sometimes lacked quantitative details (e.g., exact performance improvements, specific test coverage metrics, or how he structured his test suite). Additionally, while his background is senior‑level, the role is junior; he could have emphasized fundamentals and willingness to grow within Meta’s engineering culture. A bit more depth about his testing strategy, code review practices, and collaboration with team members would strengthen his candidacy. Overall, he communicated well and displayed relevant expertise, but a more thorough, metrics‑driven response would raise his score.
"""

client = Groq(api_key=api_key)
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b", temperature=1,
    max_completion_tokens=2048, top_p=1,
    reasoning_effort="medium", stream=True,
    stop=None, messages=[{"role": "developer", "content": "Hello world"}]
)

if "setup" not in st.session_state:
    st.session_state.setup = False


def complete_setup():
    st.session_state.setup = True

def incomplete_setup():
    st.session_state.setup = False

def show_feedback():
    st.session_state.data["feedback_shown"] = True

def display_feedback():
    st.subheader("Feedback!")
    convo_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.data["messages"]])
    feedback = client.chat.completions.create(
        model = st.session_state.model,
        messages=[
            {
                "role": "system",
                "content": """You are a helpful tool that provides feedback on an interviewee performance.
                    Before the Feedback, give a score of 1 to 10. Follow this format:
                    Overall score: <Your Score> \n
                    Feedback: <Here, you put your feedback>
                    Give only the feedback. Do not ask additional questions."""
            },
            {
                "role": "user",
                "content": f"This is the interview you need to evaluate. Keep in mind that you shouldn't engage in any conversations as there's no input (sadly) to respond to you. This is the history: {convo_history}"
            }
        ]
    )
    st.write(feedback.choices[0].message.content)



st.set_page_config(page_title="Streamlit Chat", page_icon="🤖")
st.title(":blue[Chat]:yellow[Bot]")

if not st.session_state.setup:
    if "data" not in st.session_state: 
        st.session_state.data = data = {
            "name": "Michael Jamie", "experience": "", "skills": "Python, Django, Flask, PyQT5, etc", 
            "user_message": 0, "feedback_shown": False,
            "company": "Amazon", "level": "Junior", "position": "Python Programmer", "chat_complete": False,
            "messages": []
        }
    st.subheader("Personal Information", divider="red")
    st.session_state.data["name"] = st.text_input(label="Name", placeholder="Enter your name", value=st.session_state.data["name"], max_chars=40)
    st.session_state.data["experience"] = st.text_area(label="Experience", placeholder="Describe your experience", value=st.session_state.data["experience"], max_chars=250)
    st.session_state.data["skills"] = st.text_area(label="Skills", placeholder="List your skills", value=st.session_state.data["skills"], max_chars=100)

    st.write(f"**Your name**: {st.session_state.data['name']}")
    st.write(f"**Your Experience**: {st.session_state.data['experience']}")
    st.write(f"**Your Skills**: {st.session_state.data['skills']}")

    st.write(st.session_state.data)

    st.subheader("Company and Position", divider="orange")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.data["company"] = st.selectbox("Choose Company", ("Amazon", "Meta", "Udemy", "Spotify", "Nestle", "X"))
    with col2:
        st.session_state.data["level"] = st.radio("Choose Level", options=["Junior", "Mid-level", "Senior"], key="visibility")
    with col3:
        st.session_state.data["position"] = st.selectbox("Choose position", ("Django Engineer", "Data Engineer", "ML Engineer", "AI Scientist", "Data Scientist", "Python Programmer"))

    st.button("Start Interview", on_click=complete_setup, icon="✍️")

elif st.session_state.setup and not st.session_state.data["chat_complete"] and not st.session_state.data["feedback_shown"]:
    # Interviewer Side
    st.subheader("Interviewer Side", divider="rainbow")
    st.info("You can begin by introducing yourself.", icon="👋")
    st.button("Edit Personal Information", icon="✍️", on_click=incomplete_setup)

    if "model" not in st.session_state:
        st.session_state.model = "openai/gpt-oss-120b"

    if not st.session_state.data["messages"]:
        st.session_state.data["messages"] = [
            {
                "role": "system",
                "content": f'You are a HR executive. You are interviewing a user named {st.session_state.data["name"]} for the position of {st.session_state.data["position"]} at a {st.session_state.data["level"]} level for the {st.session_state.data["company"]} company.\n\nThe interviewee has the following experience: {st.session_state.data["experience"]}.\n\nThe interviewee possesses the following skills: {st.session_state.data["skills"]}\n\nAsk each question individually, creating a conversational flow rather than presenting all the questions simultaneously.'
            }
        ]

    for message in st.session_state.data["messages"]:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    on_going = st.session_state.data["user_message"] < 5
    if on_going:
        if prompt := st.chat_input("Your answer.", max_chars=750):
            st.session_state.data["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            on_going = st.session_state.data["user_message"] < 4
            if on_going:
                with st.chat_message("ai"):
                    stream = client.chat.completions.create(
                        model=st.session_state.model, temperature=1,
                        max_completion_tokens=2048,
                        top_p=1,
                        reasoning_effort="medium",
                        stream=True,
                        stop=None,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.data["messages"]
                        ]
                    )
                    response = st.write_stream(
                        chunk.choices[0].delta.content
                        for chunk in stream
                        if chunk.choices[0].delta.content
                    )
                st.session_state.data["messages"].append({"role": "assistant", "content": response})
            st.session_state.data["user_message"] += 1

    if not on_going:
        st.session_state.data["chat_complete"] = True
        st.success("Interview completed. Thank you for your time!", icon="✅")
        if st.button("Provide Feedback", on_click=show_feedback, icon="💬"):
            st.write("Fetching feedback")

if st.session_state.data["feedback_shown"]:
    display_feedback()
