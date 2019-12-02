
import os
os.chdir("..")

import stages

BASEDIR = os.path.dirname(__file__)

def test_ctoll():
    ctoll = stages.CToLLStage()

    ctoll("%s/_dummy/dummy.c"%(BASEDIR, )) # Send llvm IR to std


def test_lltoll():
    # Receive a LLVM IR in the std
    lltoll = stages.LLToMem2RegLL()

    lltoll(std=b'''; ModuleID = './python/tests/_dummy/dummy.ll'
                    source_filename = "./python/tests/_dummy/dummy.c"
                    target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
                    target triple = "x86_64-apple-macosx10.14.0"

                    ; Function Attrs: noinline nounwind ssp uwtable
                    define i32 @a(i32 %t) #0 {
                    entry:
                    %tobool = icmp ne i32 %t, 0
                    br i1 %tobool, label %if.then, label %if.end

                    if.then:                                          ; preds = %entry
                    %add = add nsw i32 20, 20
                    %mul = mul nsw i32 %add, 2
                    %add1 = add nsw i32 20, %mul
                    br label %return

                    if.end:                                           ; preds = %entry
                    br label %return

                    return:                                           ; preds = %if.end, %if.then
                    %retval.0 = phi i32 [ %add1, %if.then ], [ 25, %if.end ]
                    ret i32 %retval.0
                    }

                    attributes #0 = { noinline nounwind ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

                    !llvm.module.flags = !{!0, !1}
                    !llvm.ident = !{!2}

                    !0 = !{i32 1, !"wchar_size", i32 4}
                    !1 = !{i32 7, !"PIC Level", i32 2}
                    !2 = !{!"clang version 8.0.0 (tags/RELEASE_800/final 375507)"}
                    ''') # Send llvm IR to std



def test_lltobc():
    # Receive a LLVM IR in the std
    lltobc = stages.LLToBC()

    lltobc(std=b'''define i32 @g(i32 %a) #0 {
                entry:
                %rem = urem i32 %a, 4
                switch i32 %rem, label %sw.epilog [
                    i32 0, label %sw.bb
                    i32 1, label %sw.bb1
                    i32 2, label %sw.bb3
                ]

                sw.bb:                                            ; preds = %entry
                %add = add i32 %a, 3
                br label %sw.epilog

                sw.bb1:                                           ; preds = %entry
                %add2 = add i32 %a, 2
                br label %sw.epilog

                sw.bb3:                                           ; preds = %entry
                %add4 = add i32 %a, 1
                br label %sw.epilog

                sw.epilog:                                        ; preds = %sw.bb3, %sw.bb1, %sw.bb, %entry
                %a.addr.0 = phi i32 [ %a, %entry ], [ %add4, %sw.bb3 ], [ %add2, %sw.bb1 ], [ %add, %sw.bb ]
                %and = and i32 %a.addr.0, 3
                ret i32 %and
                }

                    ''') # Send llvm IR to std

def test_bctoSouper():
    # Receive a LLVM IR in the std
    bctoSouper = stages.BCToSouper()
    content = open("%s/_dummy/dummy_test.bc"%(BASEDIR,), 'rb').read()
    
    bctoSouper(std=content) # Send llvm IR to std


def _test_souperCandidates():
    # Receive a LLVM IR in the std
    souperToLHS = stages.CandidatesToSouperParts(MAX_INST=1)
    
    
    souperToLHS(std=b'''
; Function: g
;[ORIGIN]   %rem = urem i32 %a, 4
%0:i32 = var
%1:i32 = urem %0, 4:i32
infer %1

; Function: g
;[ORIGIN]   %add = add i32 %a, 3
%0:i32 = var
%1:i32 = urem %0, 4:i32
pc %1 0:i32
%2:i32 = add 3:i32, %0
infer %2 (demandedBits=00000000000000000000000000000011)

; Function: g
;[ORIGIN]   %add2 = add i32 %a, 2
%0:i32 = var
%1:i32 = urem %0, 4:i32
pc %1 1:i32
%2:i32 = add 2:i32, %0
infer %2 (demandedBits=00000000000000000000000000000011)

; Function: g
;[ORIGIN]   %add4 = add i32 %a, 1
%0:i32 = var
%1:i32 = urem %0, 4:i32
pc %1 2:i32
%2:i32 = add 1:i32, %0
infer %2 (demandedBits=00000000000000000000000000000011)

; Function: g
;[ORIGIN]   %a.addr.0 = phi i32 [ %a, %entry ], [ %add4, %sw.bb3 ], [ %add2, %sw.bb1 ], [ %add, %sw.bb ]
%0 = block 4
%1:i32 = var
%2:i32 = add 1:i32, %1
%3:i32 = add 2:i32, %1
%4:i32 = add 3:i32, %1
%5:i32 = phi %0, %1, %2, %3, %4
infer %5 (demandedBits=00000000000000000000000000000011)

; Function: g
;[ORIGIN]   %and = and i32 %a.addr.0, 3
%0 = block 4
%1:i32 = var
%2:i32 = add 1:i32, %1
%3:i32 = add 2:i32, %1
%4:i32 = add 3:i32, %1
%5:i32 = phi %0, %1, %2, %3, %4
%6:i32 = and 3:i32, %5
infer %6
                        ''') # Send llvm IR to std


def test_souperIRToLLVM():
    # Receive a LLVM IR in the std
    souperToLHS = stages.SouperToLLVM()
    
    
    print(souperToLHS(std=b'''
; RHS inferred successfully
result 4294967295:i32
                        ''')) # Send llvm IR to std



def test_partial():
    # Receive a LLVM IR in the std
    lltobc = stages.LLToBC()

    bc = lltobc(std=b'''; ModuleID = 'python/tests/_paper/f3.ll'
source_filename = "python/tests/_paper/f3.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.14.0"

; Function Attrs: noinline nounwind ssp uwtable
define i32 @g(i32 %a) #0 {
entry:
  %rem = urem i32 %a, 4
  switch i32 %rem, label %sw.epilog [
    i32 0, label %sw.bb
    i32 1, label %sw.bb1
    i32 2, label %sw.bb3
  ]

sw.bb:                                            ; preds = %entry
  %add = add i32 %a, 3
  br label %sw.epilog

sw.bb1:                                           ; preds = %entry
  %add2 = add i32 %a, 2
  br label %sw.epilog

sw.bb3:                                           ; preds = %entry
  %add4 = add i32 %a, 1
  br label %sw.epilog

sw.epilog:                                        ; preds = %sw.bb3, %sw.bb1, %sw.bb, %entry
  %a.addr.0 = phi i32 [ %a, %entry ], [ %add4, %sw.bb3 ], [ %add2, %sw.bb1 ], [ %add, %sw.bb ]
  %and = and i32 %a.addr.0, 3
  ret i32 %and
}

attributes #0 = { noinline nounwind ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{!"clang version 8.0.0 (tags/RELEASE_800/final 375507)"}
''') # Send llvm IR to std

    bcToCand = stages.BCToSouper()
    print(bcToCand(std=bc).decode("utf-8"))