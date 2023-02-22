
enum Type of i32 is
    A := 10;
    B := 20;
    C := 30;
    D := 40;
end

func main -> i32 is
    var x : i32 := Type::A;
    
    println("%d", x);
    println("%d", Type::B);
    println("%d", Type::C);
    println("%d", Type::D);
    
    return 0;
end
 
