
enum Type of char is
    A; B; C; D;
end

func main -> i32 is
    var x : char := Type::A;
    
    println("%c", x);
    println("%c", Type::B);
    println("%c", Type::C);
    println("%c", Type::D);
    
    return 0;
end
 
