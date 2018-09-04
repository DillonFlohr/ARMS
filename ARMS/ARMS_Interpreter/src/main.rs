#![allow(non_snake_case)]

use std::io;
use std::fs;
use std::fs::File;
use std::io::Read;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    assert!(args.len() > 1, "Please provide a file name as an argument.");

    //Get file name
    let file_name = &args[1];

    //open file and get the contents
    let file_location_and_name = format!("{}{}","./input/", file_name.trim());
    let mut file_to_read = File::open(file_location_and_name).expect("File not found!");
	let mut file_contents = String::new();
	file_to_read.read_to_string(&mut file_contents).expect("Something went wrong while reading the file.");
    
    //Create file contents and put in ./output/file_name
    println!("Creating .cpp file...");
    let split_file_name: Vec<&str> = file_name.split('.').collect();
    let new_file_name = format!("{}{}", split_file_name[0], ".cpp");
    let new_file_location = format!("{}{}", "./output/", new_file_name);
    File::create(&new_file_location).expect("Error during file creation.");
    fs::write(new_file_location, file_contents).expect("Unable to write file");
}
