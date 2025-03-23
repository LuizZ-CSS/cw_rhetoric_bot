from app.config import MEMORY_LIMIT

def update_memory(memory_list, new_entry):
    """Maintains session memory within limits."""
    memory_list.append(new_entry)
    return memory_list[-MEMORY_LIMIT:], "\n".join(memory_list[-MEMORY_LIMIT:])
