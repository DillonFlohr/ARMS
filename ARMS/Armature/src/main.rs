#![allow(non_snake_case)]

use std::io;
use std::fs;
use std::fs::File;
use std::io::Read;
use std::env;

mod scanner;
mod parser;
mod interpreter;

fn create(file_contents: String, file_name: &String) {
    println!("Creating .cpp ODE file...");
    let split_file_name: Vec<&str> = file_name.split('.').collect();
    let new_file_name = format!("{}{}{}", split_file_name[0],"_ODE", ".cpp");
    let new_file_location = format!("{}{}", "./", new_file_name);
    File::create(&new_file_location).expect("Error during file creation.");

    //interpreter write to the file here...
    fs::write(new_file_location, file_contents).expect("Unable to write file");
}

fn get_file_contents(file_path: &String) -> String {
    println!("{}", &file_path);
    let mut file = File::open(file_path.trim()).expect("Could not open file");
    let mut file_contents = String::new();
    file.read_to_string(&mut file_contents).expect("Could not read file into string");

    return file_contents;
}

fn run_promt() {
    println!("Enter name of ARMS file to interpret: ");
    let mut file_path = String::new();
	io::stdin().read_line(&mut file_path).expect("Need to input a file path!");

    let file_contents = get_file_contents(&file_path);

    create(file_contents, &file_path);
}

fn run_file(file_path: &String) {
    let file_contents = get_file_contents(&file_path);

    create(file_contents, &file_path);
}

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        1 => run_promt(),
        2 => run_file(&args[1]),
        _ => println!("Please run with either no arguments or with one specifying the file path.")
    }

    println!("Successfully created interpreted files!")
}
