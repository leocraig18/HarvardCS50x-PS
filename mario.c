#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    int spaces;
    int hash;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    //For each row
    for (int i = 0; i < height; i++)
    {
        //Left hand side of pyramid
        for (spaces = (height - i); spaces >= 2; spaces--)
        {
            printf(" ");
        }

        for (hash = 0; hash <= (i + 1 - 1); hash++)
        {
            printf("#");
        }

        {
            printf("\n");
        }
    }
}
