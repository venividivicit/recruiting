import subprocess
import json

class QueryParser:
    def __init__(self):
        self.parser = subprocess.Popen('../queries/target/release/sedaro-nano-queries', 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, text=True)

    def parse(self, query: str) -> dict:
        normalized = ' '.join(query.split())
        self.parser.stdin.write(normalized + '\n')
        self.parser.stdin.flush()
        result = self.parser.stdout.readline()
        if not result:
            raise Exception("Parsing query failed: no result")
        return json.loads(result)

    def close(self):
        self.parser.stdin.close()
        self.parser.wait()
    