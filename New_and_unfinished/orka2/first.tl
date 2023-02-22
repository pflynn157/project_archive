import std.fs;

enum TokenType of i32 is
    None := 0;
    Eof := 1;
    Func; Is; Return; End;
    Id;
end

struct Context is
    file : i32 := 0;
    buffer : string := "";
    id_value : string := "";
end

func get_next(ctx : Context) -> i32 is
    while fs_eof(ctx.file) = false do
        var c : char := fs_get(ctx.file);
        if c = ' ' or c = '\n' then
            if strlen(ctx.buffer) = 0 then
                continue;
            end
        
            var type : i32 := TokenType::None;
            if ctx.buffer = "func" then type := TokenType::Func;
            elif ctx.buffer = "is" then type := TokenType::Is;
            elif ctx.buffer = "return" then type := TokenType::Return;
            elif ctx.buffer = "end" then type := TokenType::End;
            else
                 type := TokenType::Id;
                 ctx.id_value := ctx.buffer;
            end
            
            ctx.buffer := "";
            return type;
        else
            var buf : string := ctx.buffer;
            buf := buf + c;
            ctx.buffer := buf;
        end
    end
    return TokenType::Eof;
end

func main -> i32 is
    struct ctx : Context;
    ctx.file := fs_open("../first.txt", 1);
    if ctx.file = 0 then
        println("Error: Unable to open file.");
        return 1;
    end
    
    var token : i32 := get_next(ctx);
    while token != TokenType::Eof do
        if token = TokenType::Func then println("Func");
        elif token = TokenType::Is then println("Is");
        elif token = TokenType::Return then println("Return");
        elif token = TokenType::End then println("End");
        elif token = TokenType::Id then println("ID: %s", ctx.id_value);
        else println("IDK");
        end
        
        token := get_next(ctx);
    end
    
    fs_close(ctx.file);
    
    return 0;
end
