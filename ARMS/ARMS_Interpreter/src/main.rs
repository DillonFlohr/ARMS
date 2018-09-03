#![allow(non_snake_case)]

use std::io;
use std::fs;
use std::fs::File;
use std::io::Read;

fn main() {
    println!("Enter name of ARMS file to interpret: ");

    //Get file name
    let mut file_name = String::new();
	io::stdin().read_line(&mut file_name).expect("Need to input a file name!");

    //open file and get the contents
    let file_location_and_name = String::from("./input/".to_owned() + file_name.trim());
    let mut file_to_read = File::open(file_location_and_name).expect("File not found!");
	let mut file_contents = String::new();
	file_to_read.read_to_string(&mut file_contents).expect("Something went wrong while reading the file.");
    
    //Create file contents and put in ./output/file_name
    println!("Creating .cpp file...");
    File::create("./output/".to_owned() + file_name.trim()).expect("Error during file creation.");
    fs::write("./output/".to_owned() + file_name.trim(), file_contents).expect("Unable to write file");
}
