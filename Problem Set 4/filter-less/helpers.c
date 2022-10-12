#include "helpers.h"
#include "math.h"
#include "stdio.h"

void swap(int *a, int *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //For each collumn
    for (int i = 0; i < height; i++)
    {
        //For each pixel per collumn
        for (int j = 0; j < width; j++)
        {
            //Convert pixel to float
            float Red = image[i][j].rgbtRed;
            float Green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;

            //Find Average Value
            int average = round((Red + Green + Blue) / 3.0);
            //Set colours equal to average
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            //Convert the pixels to floats
            float Red = image[k][l].rgbtRed;
            float Green = image[k][l].rgbtGreen;
            float Blue = image[k][l].rgbtBlue;

            //Apply algorithym to colours.
            int sepiaRed = round(.393 * Red + .769 * Green + .189 * Blue);
            int sepiaGreen = round(.349 * Red + .686 * Green + .168 * Blue);
            int sepiaBlue = round(.272 * Red + .534 * Green + .131 * Blue);

            //Convert colours to sepia colours
            if (sepiaRed > 255)
            {
                (sepiaRed = 255);
            }

            if (sepiaGreen > 255)
            {
                (sepiaGreen = 255);
            }

            if (sepiaBlue > 255)
            {
                (sepiaBlue = 255);
            }
            image[k][l].rgbtRed = sepiaRed;
            image[k][l].rgbtGreen = sepiaGreen;
            image[k][l].rgbtBlue = sepiaBlue;
        }

    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Create a copy of the image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Create variables for the total neighbouring pixels
            int totalRed, totalGreen, totalBlue;
            totalRed = totalGreen = totalBlue = 0;
            float counter = 0.00;

            //Get neighbouring pixels
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int currentX = i + x;
                    int currentY = j + y;

                    //Check if pixel is valid
                    if (currentX < 0 || currentY < 0 || currentX > (height - 1) || currentY > (width - 1))
                    {
                        continue;
                    }

                    totalRed += image[currentX][currentY].rgbtRed;
                    totalGreen += image[currentX][currentY].rgbtGreen;
                    totalBlue += image[currentX][currentY].rgbtBlue;

                    counter++;

                }
                //Calculate the average of neighbouring pixels
                temp[i][j].rgbtRed = round(totalRed / counter);
                temp[i][j].rgbtGreen = round(totalGreen / counter);
                temp[i][j].rgbtBlue = round(totalBlue / counter);
            }
        }
    }
    //Copy new pixels into original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }

    return;
}

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}
