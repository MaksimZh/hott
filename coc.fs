let test3 () =
    let dep_type = Pi(Star, fun A -> Pi(A, fun _ -> A))
    let dep = Lam(fun A -> Lam(fun x -> x))
    let dep_ann = Ann(dep, dep_type)
        
    let result = infer 0 [] dep_ann
    printfn "Test 3: Type of dep: %s" (pp 0 result)
    assert (equate 0 (result, dep_type))

let Bool = Pi(Star, fun A -> Pi(A, fun _ -> Pi(A, fun _ -> A)))
let tr = Lam(fun A -> Lam(fun t -> Lam(fun f -> t)))
let fl = Lam(fun A -> Lam(fun t -> Lam(fun f -> f)))
