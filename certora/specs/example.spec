using DummyERC20A as ERC20a
using DummyERC20B as ERC20b

methods {
    name() returns string envfree;
    symbol() returns string envfree;
    decimals() returns uint8 envfree;
    asset() returns address envfree;

    totalSupply() returns uint256 envfree;
    balanceOf(address) returns uint256 envfree => DISPATCHER(true);
    nonces(address) returns uint256 envfree;

    approve(address,uint256) returns bool;
    transfer(address,uint256) returns bool;//=> DISPATCHER(true);
    transferFrom(address,address,uint256) returns bool => DISPATCHER(true);
    deposit(uint256,address);
    mint(uint256,address);
    withdraw(uint256,address,address);
    redeem(uint256,address,address);

    totalAssets() returns uint256 envfree;
    userAssets(address) returns uint256 envfree;
    convertToShares(uint256) returns uint256 envfree;
    convertToAssets(uint256) returns uint256 envfree;
    previewDeposit(uint256) returns uint256 envfree;
    previewMint(uint256) returns uint256 envfree;
    previewWithdraw(uint256) returns uint256 envfree;
    previewRedeem(uint256) returns uint256 envfree;

    maxDeposit(address) returns uint256 envfree;
    maxMint(address) returns uint256 envfree;
    maxWithdraw(address) returns uint256 envfree;
    maxRedeem(address) returns uint256 envfree;

    permit(address,address,uint256,uint256,uint8,bytes32,bytes32);
    DOMAIN_SEPARATOR() returns bytes32;

    ERC20a.balanceOf(address) returns uint256 envfree;
}



// multi contract call
// Property: any rounding error should be in favor of the system (system shoudn't lose)
rule dustFavorsTheHouse(env e, uint assetsIn, address receiver, address owner)
{
    require e.msg.sender != currentContract && receiver != currentContract;
    require totalSupply() != 0;

    uint balanceBefore = ERC20a.balanceOf(currentContract);

    uint shares = deposit(e, assetsIn, receiver);
    uint assetsOut = redeem(e, shares, receiver, owner);

    uint balanceAfter = ERC20a.balanceOf(currentContract);

    assert balanceAfter >= balanceBefore;
}



// ghost and hook
ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sstore balanceOf[KEY address addy] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances = sumOfBalances + newValue - oldValue;
}

hook Sload uint256 val balanceOf[KEY address addy] STORAGE {
    require sumOfBalances >= val;
}

// invariant
// Property: system solvency (total supply is the sum of all balances)
invariant totalSupplyIsSumOfBalances(env e)
    totalSupply() == sumOfBalances



// last revert rule
// Property: if a deposit fails, the user's balance should not change
rule depositRevertsIfNoSharesMinted(env e) {
    uint256 assets; address receiver;
    uint256 sharesBefore = balanceOf( receiver); 

    require asset() != currentContract;

    deposit@withrevert(e, assets, receiver);
    bool isReverted = lastReverted;

    uint256 sharesAfter = balanceOf( receiver);

    assert sharesBefore == sharesAfter => isReverted, "Remember, with great power comes great responsibility.";
}


/*//////////////////////////////////////////////////////////////
                            UNIT - TEST
//////////////////////////////////////////////////////////////*/

rule integrityOfTransfer(env e,address to, uint256 amount) {
    requireInvariant totalSupplyIsSumOfBalances(e);
    uint256 toBalanceBefore = balanceOf(to);
    uint256 fromBalanceBefore = balanceOf(e.msg.sender);

    transfer(e,to,amount);

    uint256 toBalanceAfter = balanceOf(to);
    uint256 fromBalanceAfter = balanceOf(e.msg.sender);

    assert (
        to != e.msg.sender => 
        (toBalanceAfter == toBalanceBefore + amount && 
        fromBalanceAfter == fromBalanceBefore - amount) 
    );

    assert (
        (to == e.msg.sender && amount != 0 ) => 
        (toBalanceAfter == toBalanceBefore && 
        fromBalanceAfter == fromBalanceBefore) 
    );
}

rule integrityOfDeposit(env e, uint256 assets, address receiver) {
    uint256 preview = previewDeposit(assets);
    uint256 balanceBefore = balanceOf(receiver);
    
    uint256 actual = deposit (e, assets, receiver);

    uint256 balanceAfter = balanceOf(receiver);

    assert preview == actual; 
    assert false;
}

/*//////////////////////////////////////////////////////////////
                        VARIABLE TRANSITIONS
//////////////////////////////////////////////////////////////*/

rule increaseOfBalanceOfUser (
        env e, 
        calldataarg args, 
        method f, 
        address user
) {
    uint256 balanceBefore = balanceOf(user);
    
    f(e,args);

    uint256 balanceAfter = balanceOf(user);

    assert (
        balanceAfter > balanceBefore => (
            f.selector == transfer(address,uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == deposit(uint256,address).selector ||
            f.selector == mint(uint256,address).selector
        )
    );
}

