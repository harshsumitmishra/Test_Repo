from klavis import Klavis
from datetime import datetime, timedelta

# Initialize Klavis client
klavis_client = Klavis(api_key="Sm/heLhqYjNCzBmKSBO5q/X1fE3JwJemo+kUyIz04e4=")

# --- 1️⃣ Google Calendar: List upcoming events ---
calendar = klavis_client.get_tool("google_calendar")  # updated method

# Define the time window
start_time = datetime(2025, 8, 28, 10, 0)
end_time = datetime(2025, 8, 28, 11, 0)

event_response = klavis_client.mcp_server.call_tools(
    server_url=calendar.server_url,
    tool_name="google_calendar_list_events",
    tool_args={
        "calendar_id": "primary",
        "min_end_datetime": start_time.isoformat(),
        "max_start_datetime": end_time.isoformat(),
        "max_results": 10
    }
)

events = event_response.get("events", [])

# Extract attendees and agenda
attendees = []
agenda = ""
for event in events:
    if "attendees" in event:
        attendees.extend([a.get("email") for a in event["attendees"]])
    if "description" in event:
        agenda += event["description"] + "\n"

# --- 2️⃣ Notion: Create a page ---
notion = klavis_client.get_tool("notion")  # updated method

notion_page_response = klavis_client.mcp_server.call_tools(
    server_url=notion.server_url,
    tool_name="notion_create_page",
    tool_args={
        "page": {
            "properties": {
                "title": "Eval All-Hands 2025-08-28"
            },
            "content": f"# Eval All-Hands 2025-08-28\n\n## Attendees\n{', '.join(attendees)}\n\n## Agenda\n{agenda}"
        }
    }
)

# Notion returns a list of blocks, extract text
notion_blocks = notion_page_response.get("blocks", [])
notion_text = ""
for block in notion_blocks:
    if block.get("type") == "text":
        notion_text += block.get("text", "") + "\n"

# --- 3️⃣ Slack: Post a message ---
slack = klavis_client.get_tool("slack")  # updated method

slack_response = klavis_client.mcp_server.call_tools(
    server_url=slack.server_url,
    tool_name="slack_bot_post_message",
    tool_args={
        "channel_id": "#general",  # or the actual channel ID
        "text": f"📌 Meeting notes for Eval All-Hands 2025-08-28:\n{notion_text}"
    }
)

print("✅ Event info posted to Slack successfully!")
