//
// Copyright 2021-2022 Patrick Flynn
// This file is part of the Tiny Lang compiler.
// Tiny Lang is licensed under the BSD-3 license. See the COPYING file for more information.
//
// Structure.cpp
// Handles parsing for structs
#include <map>

#include <parser/Parser.hpp>
#include <ast/ast.hpp>
#include <ast/ast_builder.hpp>

//
// In charge of building an enumeration declaration
//
bool Parser::buildEnum() {
    Token token = scanner->getNext();
    std::string name = token.id_val;
    
    if (token.type != Id) {
        syntax->addError(scanner->getLine(), "Expected name for enum.");
        return false;
    }
    
    // Next token should be "of"
    token = scanner->getNext();
    if (token.type != Of) {
        syntax->addError(scanner->getLine(), "Expected \"of\" after enum name.");
        return false;
    }
    
    // Get the data type
    AstDataType *dataType = buildDataType();
    
    // Next token should be "is"
    token = scanner->getNext();
    if (token.type != Is) {
        syntax->addError(scanner->getLine(), "Expected \"is\" after enum name.");
        return false;
    }
    
    // Now, scan the members
    uint64_t index = 0;
    if (dataType->getType() == V_AstType::Char) index = 'A';
    token = scanner->getNext();
    
    while (token.type != End && token.type != Eof) {
        std::string var_name = token.id_val;
        std::string enum_value = "enum_" + name + "_" + var_name;
        AstExpression *value;
        
        // Check to see if we have an assignment
        token = scanner->getNext();
        if (token.type == Assign) {
            value = buildExpression(dataType, SemiColon, true);
            switch (dataType->getType()) {
                case V_AstType::Char: index = static_cast<AstChar *>(value)->getValue(); break;
                case V_AstType::Int8: index = static_cast<AstI8 *>(value)->getValue(); break;
                case V_AstType::Int16: index = static_cast<AstI16 *>(value)->getValue(); break;
                case V_AstType::Int64: index = static_cast<AstI64 *>(value)->getValue(); break;
                
                default: index = static_cast<AstI32 *>(value)->getValue();
            }
        } else {
            switch (dataType->getType()) {
                case V_AstType::Char: value = new AstChar(index); break;
                case V_AstType::Int8: value = new AstI8(index); break;
                case V_AstType::Int16: value = new AstI16(index); break;
                case V_AstType::Int64: value = new AstI64(index); break;
                
                default: value = new AstI32(index);
            }
            
            if (token.type != SemiColon) {
                syntax->addError(scanner->getLine(), "Expected terminator after enum member.");
                token.print();
                return false;
            }
        }
        
        globalConsts[enum_value] = std::pair<AstDataType *, AstExpression *>(dataType, value);
        
        token = scanner->getNext();
        ++index;
    }
    
    return true;
}

// Parses and builds a structure
bool Parser::buildStruct() {
    Token token = scanner->getNext();
    std::string name = token.id_val;
    
    if (token.type != Id) {
        syntax->addError(scanner->getLine(), "Expected name for struct.");
        return false;
    }
    
    // Next token should be "is"
    token = scanner->getNext();
    if (token.type != Is) {
        syntax->addError(scanner->getLine(), "Expected \"is\".");
    }
    
    // Builds the struct items
    AstStruct *str = new AstStruct(name);
    token = scanner->getNext();
    
    while (token.type != End && token.type != Eof) {
        if (!buildStructMember(str, token)) return false;
        token = scanner->getNext();
    }
    
    tree->addStruct(str);
    
    return true;
}

bool Parser::buildStructMember(AstStruct *str, Token token) {
    std::string valName = token.id_val;
    
    if (token.type != Id) {
        syntax->addError(scanner->getLine(), "Expected id value.");
        token.print();
        return false;
    }
        
    // Get the data type
    token = scanner->getNext();
    if (token.type != Colon) {
        syntax->addError(scanner->getLine(), "Expected \':\' in structure member.");
        token.print();
        return false;
    }
    
    AstDataType *dataType = buildDataType();
        
    // If its an array, build that. Otherwise, build the default value
    token = scanner->getNext();
        
    if (token.type == Assign) {
        AstExpression *expr = nullptr;
        expr = buildExpression(dataType, SemiColon, true);
        if (!expr) return false;
                
        Var v;
        v.name = valName;
        v.type = dataType;
        str->addItem(v, expr);
    } else {
        syntax->addError(scanner->getLine(), "Expected default value.");
        token.print();
        return false;
    }
        
    return true;
}

bool Parser::buildStructDec(AstBlock *block) {
    Token token = scanner->getNext();
    std::string name = token.id_val;
    
    if (token.type != Id) {
        syntax->addError(scanner->getLine(), "Expected structure name.");
        return false;
    }
    
    token = scanner->getNext();
    if (token.type != Colon) {
        syntax->addError(scanner->getLine(), "Expected \':\'");
        return false;
    }
    
    token = scanner->getNext();
    std::string structName = token.id_val;
    
    if (token.type != Id) {
        syntax->addError(scanner->getLine(), "Expected structure type.");
        return false;
    }
    
    // Make sure the given structure exists
    AstStruct *str = nullptr;
    
    for (auto s : tree->getStructs()) {
        if (s->getName() == structName) {
            str = s;
            break;
        }    
    }
    
    if (str == nullptr) {
        syntax->addError(scanner->getLine(), "Unknown structure.");
        return false;
    }
    
    // Now build the declaration and push back
    vars.push_back(name);
    typeMap[name] = AstBuilder::buildStructType(structName);
    AstStructDec *dec = new AstStructDec(name, structName);
    block->addStatement(dec);
    
    // Final syntax check
    token = scanner->getNext();
    if (token.type == SemiColon) {
        return true;
    } else if (token.type == Assign) {
        dec->setNoInit(true);
        AstExprStatement *empty = new AstExprStatement;
        AstExpression *arg = buildExpression(AstBuilder::buildStructType(structName));
        if (!arg) return false;
        
        AstID *id = new AstID(name);
        AstAssignOp *assign = new AstAssignOp(id, arg);
        
        empty->setExpression(assign);
        block->addStatement(empty);
        
        // TODO: The body should only be a function call expression or an ID
        // Do a syntax check
    }
    
    return true;
}

