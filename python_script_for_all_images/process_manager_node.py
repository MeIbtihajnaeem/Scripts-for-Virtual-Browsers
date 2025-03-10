import asyncio

class ProcessManagerNode:
    def __init__(self, process_name="node"):
        self.process_name = process_name

    async def get_process_pids(self):
        """Finds PIDs of processes matching the given process name."""
        try:
            process = await asyncio.create_subprocess_exec(
                "pgrep", "-f", self.process_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            pids = stdout.decode().strip().split("\n")

            # Filter out empty results
            pids = [pid for pid in pids if pid.strip()]
            if pids:
                print(f"✅ Found PIDs for '{self.process_name}': {pids}")
            else:
                print(f"❌ No process found for '{self.process_name}'.")

            return pids

        except Exception as e:
            print(f"⚠️ Error finding process PIDs: {e}")
            return []

    async def kill_process(self):
        """Kills the process using the obtained PIDs."""
        pids = await self.get_process_pids()
        if not pids:
            return
        
        try:
            # Run kill command on all found PIDs
            await asyncio.create_subprocess_exec("kill", "-9", *pids)
            print(f"✅ Successfully killed process '{self.process_name}' with PIDs: {pids}")

        except Exception as e:
            print(f"⚠️ Error killing process '{self.process_name}': {e}")

