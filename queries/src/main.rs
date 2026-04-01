use sedaro_nano_queries::grammar;
use std::io::{self, BufRead, Write};

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = stdout.lock();
    let parser = grammar::QueryParser::new();

    for line in stdin.lock().lines() {
        let input = line.unwrap_or_else(|err| panic!("Could not read input stream! {err}"));
        if input.is_empty() { continue; }

        let query = parser
            .parse(&input)
            .unwrap_or_else(|err| panic!("Could not parse input! {err}"));

        let output = serde_json::to_string(&query).unwrap();
        out.write_all(output.as_bytes()).unwrap();
        out.write_all(b"\n").unwrap();
        out.flush().unwrap();
    }
}