# Properties of ERC4626 
Descriptions: ERC-4626 is a standard to optimize and unify the technical parameters of yield-bearing vaults. It provides a standard API for tokenized yield-bearing vaults that represent shares of a single underlying ERC-20 token. ERC-4626 also outlines an optional extension for tokenized vaults utilizing ERC-20, offering basic functionality for depositing, withdrawing tokens and reading balances. ([source](https://ethereum.org/en/developers/docs/standards/tokens/erc-4626/))
## Valid State
- [ ] **Deposited** (when balanceOf user > 0)
- [ ] **NotDepositedOrWithdrawn** (when balanceOf user == 0)
- [ ] **Empty** (when asset.balanceOf(this) == 0)
- [ ] **Fill** (when asset.balanceOf(this) > 0) 

## State Transitions 
- [ ] User can withdraw after they deposited
- [ ] User cannot withdraw the same amount twice after they withdraw more than half of their assets 
- [ ] Deposit will increase the shares of user

## Variable Transitions
- [ ] User assets can decrease only by User him/herself, address with allowance, and operator (address with max uint256 allowance)
- [ ] User assets can decrese only through redeem() and withdraw()
- [ ] User assets can increased only through deposit() and mint()
- [ ] totalAssets() can only increase throgh deposit(), mint() and accrueRewards() (NOTE: since ERC20 transfer exist someone still can transfer their assets through ERC20.transfer or transferFrom) 
- [ ] totalAssets() can only decrese through redeem() and withdraw()
- [ ] deposit() and mint() will revert if users aren't receiveing any shares 

## High Level Properties 
- [ ] totalAssets will always greater than individual assets 
- [ ] As long as user have shares they can always withdraw it
- [ ] withdraw will not affect other user assets
- [ ] deposit will not affect other user assets

## Unit Test
- [ ]