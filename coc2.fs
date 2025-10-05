let test5 () =
    let id_type = Pi(Star, fun A -> Pi(A, fun _ -> A))
    let id = Lam(fun A -> Lam(fun x -> x))
    let id_ann = Ann(id, id_type)
        
    let result = infer 0 [] id_ann
    printfn "Test 5: Type of id: %s" (pp 0 result)
    assert (equate 0 (result, id_type))
