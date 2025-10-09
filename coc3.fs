// let add (m: Nat) (n: Nat) = {
//     Apply = fun next initial ->
//         m.Apply next (n.Apply next initial)
// }

let add = Lam(fun m -> Lam(fun n ->
            Lam(fun A -> 
                Lam(fun s -> Lam(fun z -> 
                    Appl(
                        Appl(Appl(m, A), s),
                        Appl(
                            Appl(Appl(n, A), s),
                            z
                        )
                    ))))))
let add_type = Pi(Nat, fun _ -> Pi(Nat, fun _ -> Nat))
let add_ann = Ann(add, add_type)
