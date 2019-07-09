use std::env;
use rustc_demangle::demangle;

fn main() {
    let args: Vec<String> = env::args().collect();
    let demangled = demangle(&args[1]);
    println!("{}", demangled);
}
