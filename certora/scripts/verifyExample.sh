if [[ "$1" ]]
then
    RULE="--rule $1"
fi

if [[ "$2" ]]
then
    MSG="- $2"
fi

solc-select use 0.8.0
certoraRun \
    certora/harnesses/mixins/ERC4626BalanceOfHarness.sol \
    certora/helpers/DummyERC20A.sol certora/helpers/DummyERC20B.sol \
    --verify ERC4626BalanceOfHarness:certora/specs/example.spec \
    --optimistic_loop \
    --loop_iter 3 \
    --send_only \
    --cloud \
    --rule_sanity \
    $RULE \
    --msg "ERC4626 verification: $RULE $MSG"


# certora/harnesses/mixins/ERC4626BalanceOfHarness.sol \
# certora/harnesses/mixins/ERC4626AccountingHarness.sol \