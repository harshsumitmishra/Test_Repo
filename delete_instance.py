from klavis import Klavis

# Initialize Klavis client
client = Klavis(api_key="Sm/heLhqYjNCzBmKSBO5q/X1fE3JwJemo+kUyIz04e4=")

# Define the instance ID to delete
instance_id = "197a4951-08b7-4972-a10a-304d4b41e3f5"

# Attempt to delete the instance
try:
    response = client.mcp_server.delete_server_instance(instance_id)
    print(f"Instance {instance_id} deleted successfully: {response}")
except Exception as e:
    print(f"Error deleting instance {instance_id}: {e}")
